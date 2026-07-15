YAAW: Yet Another Argyll Wrapper (or Workflow)
YAAW is deliberately simple, lightweight printer profiling wrapper using the ArgyllCMS colour
management software written by Graeme Gill of Argyll CMS in Melbourne, Australia. It is
designed to be portable across platforms. Its approach is perhaps along the lines of LittleArgyllGUI,
and it is religiously committed to a KISS strategy, transparent in its operation, and written in pure
Python with tkinter. Directly or indirectly, however, YAAW provides access to the full range of
relevant ArgyllCMS printer profiling commands and settings, with man pages for each Argyll tool
being accessible from the configuration page for reference. Developed and tested under both Linux
Mint and macOS, other platforms should work in principle but may need path/default-command
adjustments.
The initial Configuration screen provides editable presets for the most common options for each of
the Argyll tools, with each tool having an additional field for adding further arguments if required.
Profile directory names are auto-generated based on the contents of the Printer/Paper/Ink fields,
with the filenames and internal description fields adding "Argyll_<instrument>_<patchcount>" to
the directory name. This allows multiple profile runs at different patch densities and/or instruments
to coexist, while also recording how each profile was generated, identifiably stored within a
sensibly named parent directory. To simplify startup, a config from a similar session can be loaded
at the Configuration screen and the Paper Name simply edited to suit the new job before
proceeding.
Patchcount and papersize settings are included for several instruments, although the default is for
the ColorMunki. Targets are sized for A3 paper which is then printed condensed onto A4, with the
target generated at the larger nominal page size, then printed scaled down by the printer/print
workflow. Likewise, the A2R papersize may be printed onto A3 paper. The targets using the
ColorMunki allow 460 patches on a single A4 page, or 960 patches on a single A3 page. The A2R
patch layout is rotated 90 degrees so patches, once printed onto A3 paper can be read using a guide
sized for A4 paper. Potential also exists to further condense patch densities with the printtarg “-a”
argument, although this requires configuration via the “Additional Arguments” field. A guide for the
ColorMunki or similar spectrophometer is essential with these condensed targets, but even at these
higher densities, strip reading has proven to be 100% reliable. Alternatively, the standard Argyll
patch counts for each page size may be selected and the targets printed at the standard defaults of
210 or 420 patches per A4 or A3 page.
An option is available to inspect the Argyll commands prior to execution. Extensive logs are also
maintained. Each profiling session is automatically recorded as a suitably named JSON file
containing the complete configuration used to generate that profile. These also allow for an initial
"printing session" where targets for as many papers as desired can be printed sequentially, with the
targets subsequently being read and the ICC profiles generated once the targets are properly dried.
Once an ICC profile has been created, a simple static gamut viewer is available to graphically view
the profile limits and other pertinent metrics. YAAW tests for and warns against inadvertent
overwriting of previously generated data, and includes crash recovery, restarting from the last active
step in the event of a system failure.
Default directory locations are probably sensible in most instances but may be edited at the top of
the script if necessary. Although developed using an x-rite ColorMunki, YAAW is equally
applicable for use with other spectrophotometers - although some of the "Patch" presets may need
adjustment (other patch values can be entered manually and will be saved in the JSON config file)
YAAW does not attempt to hide ArgyllCMS. Instead, it provides a structured workflow around the
standard Argyll tools while keeping all generated commands visible and editable.
