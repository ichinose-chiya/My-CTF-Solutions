import angr

proj = angr.Project('./00_angr_find')
simgr = proj.factory.simgr(proj.factory.entry_state())
simgr.explore(find = 0x80492F0)

if simgr.found:
    print(simgr.found[0].posix.dumps(0))
else:
    print("Solution not found!")
