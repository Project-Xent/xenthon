set_project("xenthon")
set_version("0.4.0")
set_languages("c17")
set_allowedplats("mingw")

option("xent")
    set_default("..")
    set_showmenu(true)
    set_description("Directory holding xent-core, xent-kit and fluxent")
option_end()

option("xent_lib_dir")
    set_default("")
    set_showmenu(true)
    set_description("Directory holding the prebuilt xent static libraries")
option_end()

option("python_lib_dir")
    set_default("")
    set_showmenu(true)
    set_description("Directory holding python3.lib for the target architecture")
option_end()

local xent_libs = {
    "fluxent", "xtk", "xent_core", "cwinrt-rt",
    "cwinrt-bindings-foundation",
    "cwinrt-bindings-ui-composition",
    "cwinrt-bindings-ui-composition-interactions",
    "cwinrt-bindings-ui-viewmanagement",
    "cwinrt-bindings-globalization",
    "cwinrt-bindings-globalization-datetimeformatting",
    "cwinrt-bindings-globalization-numberformatting",
    "cwinrt-bindings-ui-input",
}

rule("cython")
    add_deps("c")
    set_extensions(".pyx")
    before_buildcmd_file(function (target, batchcmds, sourcefile, opt)
        local python = target:data("python")
        local module = "xenthon." .. path.basename(sourcefile)
        local cfile = path.join(target:autogendir(), path.basename(sourcefile) .. ".c")
        local objectfile = target:objectfile(cfile)
        table.insert(target:objectfiles(), objectfile)
        batchcmds:show_progress(opt.progress, "${color.build.object}cython %s", sourcefile)
        batchcmds:mkdir(path.directory(cfile))
        batchcmds:vrunv(python, {"-m", "cython", "-3", "-I", "src", "--module-name", module, "-o", cfile, sourcefile})
        batchcmds:compile(cfile, objectfile)
        batchcmds:add_depfiles(sourcefile, table.unpack(os.files(path.join(path.directory(sourcefile), "*.pxi"))))
        batchcmds:add_depfiles(path.join(path.directory(sourcefile), "_xent.pxd"))
        batchcmds:set_depmtime(os.mtime(objectfile))
        batchcmds:set_depcache(target:dependfile(objectfile))
    end)
rule_end()

target("_reconcile")
    set_kind("shared")
    set_prefixname("")
    set_extension(".pyd")
    add_rules("cython")
    add_files("src/xenthon/_reconcile.pyx")
    add_defines("Py_LIMITED_API=0x030C0000")
    add_cflags("-Wno-unused-function", "-Wno-unreachable-code-fallthrough", { force = true })
    on_load(function (target)
        import("lib.detect.find_tool")
        local python = assert(find_tool("python"), "python not found")
        local info = os.iorunv(python.program, {"-c", "import sys, sysconfig; print(sysconfig.get_path('include')); print(sys.base_prefix)"}):split("\n")
        target:data_set("python", python.program)
        target:add("includedirs", info[1]:trim())
        local pylibs = get_config("python_lib_dir")
        target:add("linkdirs", (pylibs and pylibs ~= "") and pylibs or path.join(info[2]:trim(), "libs"))
        local xent = get_config("xent")
        for _, pkg in ipairs({"xent-kit", "xent-core", "fluxent"}) do
            target:add("includedirs", path.join(xent, pkg, "include"))
        end
        local lib_dir = get_config("xent_lib_dir")
        if not lib_dir or lib_dir == "" then
            lib_dir = path.join(xent, "fluxent", "build", "mingw", "x86_64", is_mode("debug") and "debug" or "release")
        end
        target:add("linkdirs", lib_dir)
        if os.isfile(path.join(lib_dir, "libxent.a")) then
            target:add("links", "xent")
        else
            target:add("links", table.unpack(xent_libs))
        end
    end)
    add_links("python3")
    add_syslinks("user32", "gdi32", "dcomp", "d2d1", "d3d11", "dxgi", "dwrite", "dwmapi", "ole32", "oleaut32",
                 "uuid", "uxtheme", "imm32", "advapi32", "shell32", "coremessaging", "uiautomationcore",
                 "runtimeobject", "windowscodecs")
    after_build(function (target)
        os.cp(target:targetfile(), path.join(os.projectdir(), "src", "xenthon"))
    end)
target_end()
