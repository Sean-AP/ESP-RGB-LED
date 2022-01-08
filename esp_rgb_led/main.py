from .led import led, lookup, random
from .parser import parse
from .setup_net import NAME, PORT
from .setup_led import MAX_FILESIZE
import uasyncio
import gc

parse_task = None
exec_task = None

ping = bytearray(b"ping")
buf = bytearray(MAX_FILESIZE)

vars = { "r" : 0, "g" : 0, "b" : 0 }


# Main routine
async def main(vars, reader, writer):
    global buf, ping, exec_task

    # Accept and decode request
    print("Accepted a connection")

    try:
        read = await reader.readinto(buf)
        print("Received {0} bytes".format(read))

        # Check for API ping
        if read == len(ping) and buf[:len(ping)] == ping:
            print("Responding to ping")
            await ping_response(exec_task, vars, writer)
            return

        func = await parse_buf(read)
        await exec_func(func)

    # Catch this task getting cancelled by the next request
    except uasyncio.CancelledError:
        print("Task cancelled by a new connection")

    # Catch any other error
    except Exception as e:
        fail(str(e))

    # Close streams on completion
    finally:
        reader.close()
        writer.close()

        # Cleanup on exit
        gc.collect()
        gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())


# Parse the given buffer, cancelling any ongoing parsing task
async def parse_buf(read: int):
    global buf, parse_task

    if parse_task is not None:
        print("Cancelling current parse task")
        parse_task.cancel()

    parse_task = uasyncio.current_task()
    func = parse(buf[:read].decode("ascii"))
    parse_task = None

    gc.collect()
    gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

    print("Parsed script:")
    print(func)
    return func


# Run a parsed script, cancelling any ongoing execution task
async def exec_func(func: str):
    global vars, exec_task

    if exec_task is not None:
        print("Cancelling current exec task")
        exec_task.cancel()

    print("Executing new script")
    exec_task = uasyncio.current_task()
    
    exec(func)
    await locals()['__script'](vars, led, lookup, random)
    
    exec_task = None
    print("Execution finished")

    # Remove additional vars to reclaim space
    vars = { "r" : vars["r"], "g" : vars["g"], "b" : vars["b"] }
    gc.collect()
    gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

    


# Respond to a ping request from the site
# The program will write the device name, whether the colour is currently static, the current colour
async def ping_response(task, vars: dict, writer):
    writer.write("{{\n\t\"name\": \"{0}\",\n\t\"static\": {1},\n\t\"colour\": [{2},{3},{4}]\n}}".format(
        NAME,
        str(task is None).lower(),
        lookup[vars["r"]],
        lookup[vars["g"]],
        lookup[vars["b"]]
    ))

    await writer.drain()


# Set LEDs to red and print error message on failure
def fail(err: str):
    print(err)

    led[0].duty(1023)
    led[1].duty(0)
    led[2].duty(0)


# On executing, start a TCP socket
if __name__ == "__main__":    
    loop = uasyncio.get_event_loop()
    loop.create_task(
        uasyncio.start_server(lambda reader, writer: main(vars, reader, writer), "0.0.0.0", PORT, backlog=1)
    )

    print("Listening on port {0}".format(PORT))
    loop.run_forever()
    loop.close()