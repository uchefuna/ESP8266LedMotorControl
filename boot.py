#

# turn off vendor OS debugging messages
import gc
import machine  # type: ignore
import esp
esp.osdebug(None)  # type: ignore

print(f"\n\nCurrent frequency of the CPU: {machine.freq()}\n")
# machine.freq()          # get the current frequency of the CPU
# machine.freq(160000000) # set the CPU frequency to 160 MHz

# garbage collector
print(f"gabbage collected: {gc.collect()}\n")
