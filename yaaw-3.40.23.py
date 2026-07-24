#!/usr/bin/env python3
"""
Interactive Printer Profiling GUI for ColorMunki or similar
Wraps ArgyllCMS tools with automatic field population and crash recovery

Features:
- Automatic field population based on printer/paper/ink selection
- Session persistence and crash recovery
- Support for 210, 420, 460, 840, 920, 960, 1680, 1840, 1920, or custom patch targets
- Configurable output directory
- ICC profile preconditioning support
- Automatic opening of print targets in image viewer

Version: 3.40.23

Copyright: Richard Lindner and contributors
Coding assistance: Anthropic Claude; OpenAI ChatGPT
License: MIT

3.39P.11: Successful project/config loads now update the screen silently; failed loads still show errors.
3.39.13: Startup autosizing now uses a fixed sensible preferred width instead of expanding to Tk's full requested widget width on large displays.
3.39.14: Patch-layout selector now sizes its Treeview rows/popup from actual font metrics to avoid clipped rows on high-DPI or large-font desktops.
3.39.15: Patch-layout tables are now instrument-specific; non-CM instruments use clearly marked placeholder tables ready for experimental values. Instrument is now manually editable.
3.39.16: Paper Size is now manually editable; generated filenames/descriptions now include instrument code.
3.39.17: Added A3R paper size alias, mapping to 420x297 for rotated A3 printtarg layouts.
3.39.18: Replaced narrow system message boxes with compact YAAW dialogs for easier reading.
3.39.19: chartread now enables -H by default only for CM/ColorMunki; i1/i1Pro and 3p/i1Pro3+ omit -H unless manually added in Additional chartread Args.
3.39.20: Added a linked Instrument selector beside the Basic Information heading so the target instrument is chosen before other settings.
3.39.21: Kept the scrollable configuration page fitted to the visible canvas width so right-aligned header controls remain visible.
3.39.22: Preconditioning Profile now defaults blank: blank omits targen -c and uses Argyll's default model, literal none passes -c none, and ICC/MPP paths pass normally. Hardened subprocess output handling against stdout/stderr pipe deadlocks; workflow workers now use main-thread configuration snapshots instead of reading Tk variables.
3.39.23: Project config loading now restores the saved basename and paths exactly instead of re-running auto-naming and silently converting legacy -Argyll_<patches> projects to -Argyll_<instrument>_<patches>.
3.39.29: Gamut Viewer L*a* and L*b* panels are now wide, shallower side views so their hull proportions read more naturally while the top panels remain square.
3.39.31: Gamut Viewer is now fully resizable; plots redraw to the available space and side-view L* guide labels use a protected left gutter.
3.39.25: Gamut Viewer now uses a 2x2 layout with the a*b* plot and profile metrics at the top, plus separate L*a* and L*b* side views below.
3.39.26: Gamut Viewer metrics now occupy a full-size fourth panel with larger text; sRGB and AdobeRGB references use more distinct colours and dash patterns; L* slice levels are lightly marked on both side views.
3.39.28: Gamut Viewer removes a*b* slice overlays, uses a true 0-100 L* scale in side views, separates reference labels, and scales larger on taller displays.
3.39.27: Fixed a legend background error that stopped gamut plots rendering; equal-size 2x2 panels now scale to the available screen height.
3.39.24: Startup now locates manual ArgyllCMS installations in common locations, adds the discovered bin directory to YAAW's PATH, and retains the matching HTML documentation directory. Help buttons prefer installed man pages, then local HTML, and ask before opening official online documentation.
3.40.0: Stable release of the resizable four-panel Gamut Viewer with responsive plots, clearer reference markers, L* guides, and scalable metrics text.
3.40.1: Internal build: Step 3 chartread terminal now closes automatically when chartread exits; removed the redundant modal launch acknowledgement.
3.40.2: Local and confirmed online HTML documentation now requests a new browser window rather than a new tab, while remaining browser- and distribution-neutral.
3.40.3: Internal build: chartread now runs in a YAAW pseudo-terminal window on Linux/macOS; external terminal launch remains as fallback. The live window retains the complete session, while the project log records concise instrument/calibration information plus warnings and errors. chartread terminal bell cues are replayed through Tk, and the window closes automatically after a clean exit. Carriage-return progress counters are condensed into space-separated lines in the screen and project logs.
3.40.3-internal4: View Log now toggles the main Execution display between the persistent project logfile and an independent live-output buffer; no separate viewer window is opened.
3.40.3-internal6: Bold, slightly enlarged labels are limited to the main navigation/header controls and the Execution page workflow/control rows; in-form Browse and Help buttons retain the normal font.
3.40.3-internal7: Main navigation and Execution action buttons use a persistent bold font at exactly the normal interface text size; in-form buttons remain unchanged.
3.40.4: Help buttons now display ArgyllCMS HTML documentation in a built-in Tk viewer window instead of handing off to an external web browser. Local documentation pages can be followed and navigated in place; a confirmed online page is shown read-only, with any links on it opened in the system browser rather than fetched automatically.
3.40.5: Local HTML documentation that exists but isn't readable by the current user (e.g. ArgyllCMS unpacked as root under /opt) is now detected before attempting to display it. The online-documentation prompt explains the permission problem and gives the chmod command to fix it, instead of the viewer just showing a raw PermissionError.
3.40.6: Dropped the optional tkinterweb dependency entirely (not packaged for Ubuntu/Mint). The documentation viewer now always uses YAAW's own native-tkinter HTML renderer, with no external package required or used.
3.40.7: Fixed a documentation-viewer bug where pages rendered completely blank. The renderer was treating void elements like <meta> and <link> (which have no closing tag) as depth-tracked "skip" regions; any <head> with more than one <meta> tag - i.e. almost every real HTML page - left the skip counter stuck above zero, silently suppressing the entire rest of the document including <body>.
3.40.8: Fixed internal HTML links not resolving. In-page anchor links (href="#Section", e.g. a "Usage" contents list at the top of a command's doc page) previously did nothing at all. The renderer now tracks id="..." and <a name="..."> targets while parsing and scrolls to them, both for same-page "#fragment" links and for cross-page links like "colprof.html#Notes".
3.40.9: The documentation viewer's Back button is now greyed out whenever there's nowhere to go back to (i.e. before you've followed a link within the viewer). Previously it was always clickable but silently did nothing until you had navigated forward at least once, which looked identical to it being broken.
3.40.10: Fixed Back doing nothing after following an in-page anchor link (e.g. jumping from a "Usage" contents list down to a heading on the same page). Anchor jumps are now recorded in the viewer's navigation history alongside full page loads, so Back correctly scrolls back to where you were before the jump - matching ordinary browser behaviour.
3.40.11: Added an Exit button at the extreme top right, immediately after Load Config.
3.40.12: Added chartread -r resume and -p patch-by-patch controls; introduced a restrained portable visual refresh with a lighter neutral background, clearer hint text, stronger section headings, slightly airier spacing, accented workflow buttons, and improved monospaced execution displays.
3.40.13: Removed redundant help-row hint text and right-aligned the targen, printtarg, chartread, and colprof Help buttons.
3.40.14: Step 4 now records the first ten lines of profcheck -v2 -s -w output in the persistent project log, without displaying that detailed worst-patch report in the main Execution window.
3.40.15: Restored the chartread terminal Text widget to platform-native styling and reinforced focus/Return routing, fixing a macOS Aqua/Tk regression where the calibration prompt opened but keyboard input did not reach chartread.
3.40.16: Step 3 now asks ArgyllCMS to enumerate connected instruments before opening chartread, aborting cleanly when no device is found or when the connected device does not match the selected CM/i1/3p instrument family.
3.40.17: Step 3 instrument preflight now runs before any file-overwrite warning, so missing or mismatched hardware is reported before the user is asked about existing output files.
3.40.18: The detailed profcheck run now includes labelled Lab axes and exposes its generated interactive X3DOM through a browser-launch button that appears only while viewing the persistent project log.
3.40.19: Swapped the logfile-view Live Output and X3DOM button positions so View Log and Live Output occupy the same screen position.
3.40.20: The persistent profcheck summary now retains the harmless patch-count line without counting it against the ten highest delta-E result entries.
3.40.21: Gamut Viewer now asks iccgamut to generate an independent X3DOM gamut model and provides a 3D Gamut browser button within the Profile Metrics panel. The passive Execution and About text panes now set explicit foreground, background, cursor, and selection colours to avoid platform/theme contrast mismatches. The Execution screen now groups the persistent logfile, Show Gamut, and 3D Error Map under a Details mode. Clear Window and Current Settings are hidden while Details is shown, so the Details/Live Output toggle occupies the same screen position in both modes. Details is enabled for a loaded project when its completed working ICC exists, and after a successful Step 4: beginning any new workflow step invalidates and disables it. When Details is opened for an older completed project lacking the profcheck X3DOM file, YAAW generates the 3D Error Map on demand from the existing TI3 and ICC without rebuilding the profile.
3.40.22: Code freeze (?)
3.40.23:  Loading any project JSON now resets the Execution page to Live Output before applying the new project, preventing stale Details content from the previously loaded session.

"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
import subprocess
import shlex
import threading
import codecs
import select
import signal
import shutil
from pathlib import Path
from datetime import datetime
import re
import sys
import webbrowser
from html.parser import HTMLParser


class _ArgyllHtmlParser(HTMLParser):
    """Minimal HTML-to-Tk renderer using only the Python standard library
    and native tkinter widgets - no external HTML/browser packages.

    This is not a general-purpose HTML engine. It understands enough of
    the small, hand-written markup used by ArgyllCMS's own documentation
    pages - headings, paragraphs, lists, <pre>, simple tables, and links -
    to display them readably inside a Tk Text widget.
    """

    _SKIP_TAGS = {'script', 'style', 'head', 'title'}
    _HEADING_TAGS = {'h1': 'h1', 'h2': 'h2', 'h3': 'h3', 'h4': 'h4', 'h5': 'h4', 'h6': 'h4'}
    _INLINE_TAGS = {'b': 'b', 'strong': 'b', 'i': 'i', 'em': 'i', 'code': 'code'}

    def __init__(self, text_widget, on_link):
        super().__init__(convert_charrefs=True)
        self.text = text_widget
        self.on_link = on_link
        self._style_stack = []
        self._skip_depth = 0
        self._pre_depth = 0
        self._link_href = None
        self._link_counter = 0
        self._at_line_start = True
        self._last_was_space = True
        # Maps anchor name (from id="..." or <a name="...">) to the Tk
        # text index where it occurs, so in-page "#fragment" links can
        # scroll to the right spot instead of silently doing nothing.
        self.anchors = {}

    def _write(self, s, extra_tags=()):
        if self._skip_depth or not s:
            return
        tags = tuple(self._style_stack) + tuple(extra_tags)
        self.text.insert('end', s, tags)
        self._at_line_start = s.endswith('\n')
        self._last_was_space = s[-1] in ' \t\n\r\f\v'

    def _newline(self, n=1):
        if self._at_line_start:
            return
        self._write('\n' * n)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        anchor_name = attrs.get('id') or (attrs.get('name') if tag == 'a' else None)
        if anchor_name:
            self.anchors[anchor_name] = self.text.index('end')
        if tag in self._SKIP_TAGS:
            self._skip_depth += 1
            return
        if tag == 'br':
            self._write('\n')
            self._at_line_start = True
        elif tag in ('p', 'div'):
            self._newline(2)
        elif tag in self._HEADING_TAGS:
            self._newline(2)
            self._style_stack.append(self._HEADING_TAGS[tag])
        elif tag in self._INLINE_TAGS:
            self._style_stack.append(self._INLINE_TAGS[tag])
        elif tag == 'hr':
            self._newline(1)
            self._write('\u2500' * 70 + '\n')
        elif tag == 'pre':
            self._newline(1)
            self._pre_depth += 1
            self._style_stack.append('pre')
        elif tag == 'li':
            self._newline(1)
            self._write('  \u2022 ')
        elif tag == 'tr':
            self._newline(1)
        elif tag in ('td', 'th'):
            self._write('   ')
        elif tag == 'a':
            self._link_href = attrs.get('href')

    def handle_endtag(self, tag):
        if tag in self._SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if tag in self._HEADING_TAGS:
            if self._style_stack and self._style_stack[-1] == self._HEADING_TAGS[tag]:
                self._style_stack.pop()
            self._newline(2)
        elif tag in self._INLINE_TAGS:
            want = self._INLINE_TAGS[tag]
            if self._style_stack and self._style_stack[-1] == want:
                self._style_stack.pop()
        elif tag == 'pre':
            if self._style_stack and self._style_stack[-1] == 'pre':
                self._style_stack.pop()
            self._pre_depth = max(0, self._pre_depth - 1)
            self._newline(1)
        elif tag in ('p', 'div', 'table'):
            self._newline(2)
        elif tag == 'a':
            self._link_href = None

    def handle_data(self, data):
        if self._skip_depth:
            return
        if self._pre_depth:
            self._write(data)
            return
        if not data:
            return
        leading_ws = data[0] in ' \t\r\n\f\v'
        trailing_ws = data[-1] in ' \t\r\n\f\v'
        core = ' '.join(data.split())
        if not core:
            # A whitespace-only run between elements/tags; collapse it to
            # at most a single boundary space.
            if not self._last_was_space:
                self._write(' ')
            return
        if leading_ws and not self._last_was_space:
            self._write(' ')
        if self._link_href:
            self._link_counter += 1
            tagname = f'link{self._link_counter}'
            self._write(core, extra_tags=('link', tagname))
            href = self._link_href
            self.text.tag_bind(tagname, '<Button-1>', lambda e, h=href: self.on_link(h))
            self.text.tag_bind(tagname, '<Enter>', lambda e: self.text.config(cursor='hand2'))
            self.text.tag_bind(tagname, '<Leave>', lambda e: self.text.config(cursor='arrow'))
        else:
            self._write(core)
        if trailing_ws:
            self._write(' ')


# === User-editable path defaults ===========================================
#
# WORKING_ROOT is where YAAW stores per-job Argyll files:
# .ti1, .ti2, .ti3, print targets, project JSON, and run logs.
#
# ICC_OUTPUT_ROOT is where finished ICC profiles are copied/installed.
#
# PROFILE_BROWSE_ROOT is the default starting point when browsing for existing
# ICC profiles, rendering profiles, or preconditioning profiles.
#
# SESSION_FILE is the transient crash-recovery session saved while editing.

WORKING_ROOT = Path(os.path.expanduser("~/ColourManagement/YAAW"))
ICC_OUTPUT_ROOT = Path(os.path.expanduser("~/.local/share/color/icc"))
PROFILE_BROWSE_ROOT = Path(os.path.expanduser("~/ColourManagement"))
SESSION_FILE = Path(os.path.expanduser("~/tmp/.prtrprof_session.json"))


def strip_argyll_suffix(name):
    """Strip generated -Argyll suffixes from a profile/job name.

    Accepts the older -Argyll and -Argyll_<patches> forms and the newer
    -Argyll_<instrument>_<patches> form, so legacy project folders continue
    to collapse back to Printer_Paper_Ink.
    """
    return re.sub(r'-Argyll(?:_[A-Za-z0-9]+)?(?:_\d+)?$', '', name or '')


def safe_filename_token(value, fallback='custom'):
    """Return a compact filename-safe token for generated name parts."""
    token = re.sub(r'[^A-Za-z0-9]+', '', str(value or '').strip())
    return token or fallback


def printtarg_paper_size_arg(display_value):
    """Translate GUI paper-size labels to printtarg -p arguments.

    A3R and A2R are user-facing labels for sheets specified with their
    dimensions swapped so printtarg lays them out rotated by 90 degrees.
    A3R maps to 420x297; A2R maps to 594x420.  Legacy configs that still
    contain the literal dimension values are accepted unchanged.
    """
    value = (display_value or '').strip()
    if value == 'A3R':
        return '420x297'
    if value == 'A2R':
        return '594x420'
    return value


# Instrument-specific empirical layout tables.
#
# Structure:
#   INSTRUMENT_LAYOUTS['CM'][(paper_size, patch_count)] = 'layout guidance'
#
# CM is the tested ColorMunki table.  Other instruments are deliberately
# populated with obvious PLACEHOLDER rows so they can be experimentally tested
# and edited without changing the selector code.
INSTRUMENT_LAYOUTS = {
    'CM': {
        ('A4', '210'):     '1 x A4 normal',
        ('A4', '420'):     '2 x A4 normal',
        ('A4', '630'):     '3 x A4 normal',
        ('A4', '840'):     '4 x A4 normal',
	    ('A4', '1260'):	   '6 x A4 normal', 
        ('A4', '1680'):    '8 x A4 normal',

#        ('A3', '420'):     '1 x A3, potentially condensed to A4',
        ('A3', '460'):     '1 x A3, potentially condensed to A4',
        ('A3', '920'):     '2 x A3, potentially condensed to A4',
        ('A3', '1380'):    '3 x A3, potentially condensed to A4',
        ('A3', '1840'):    '4 x A3, potentially condensed to A4',

#        ('A2R', '920'):    '1 x A2R rotated, potentially condensed to A3',
        ('A2R', '960'):    '1 x A2R rotated, potentially condensed to A3',
        ('A2R', '1920'):   '2 x A2R rotated, potentially condensed to A3',

        ('Letter', '180'):  '1 x Letter-class normal',
        ('Letter', '388'):  '2 x Letter-class normal',
        ('Letter', '576'):  '3 x Letter-class normal',
        ('Letter', '764'):  '4 x Letter-class normal',

        ('11x17', '433'):  '1 x 11x17-class normal',
        ('11x17', '883'):  '2 x 11x17-class normal',
        ('11x17', '1353'): '3 x 11x17-class normal',
        ('11x17', '1803'): '4 x 11x17-class normal',
    },

    # PLACEHOLDER tables.  These are intentionally not claimed as tested.
    # Replace/add rows here as instrument-specific printtarg behaviour is
    # experimentally confirmed.
    'i1': {
        ('A4', '440'):     '1 x A4 normal',
        ('A4', '880'):     '2 x A4 normal',
        ('A4', '1320'):    '3 x A4 normal',
        ('A4', '1760'):    '4 x A4 normal',
#        ('A3', '672'):     '1 x A3 normal',
        ('A3R', '980'):    '1 x A3R rotated normal',
        ('A3R', '1960'):   '2 x A3R rotated normal',
        ('A3R', '2940'):   '3 x A3R rotated normal',
#        ('A2R', '1440'):   '1 x A2R rotated normal',
    },
    '3p': {
#        ('A4', '90'):      '1 x A4 normal',
#        ('A4', '180'):      '2 x A4 normal',
#        ('A4', '270'):      '3 x A4 normal',
#        ('A4', '360'):      '4 x A4 normal',
#        ('A3', '144'):     '1 X A3 normal',
#        ('A3R', '200'):    '1 x A3R rotated, normal',
#        ('A3R', '400'):    '2 x A3R rotated, normal',
#        ('A3R', '600'):    '3 x A3R rotated, normal',
#        ('A2R', '306'):    '1 x A2R rotated, normal',
    },
#    'SS': {
#        ('A4', '1170'):     '1 x A4 normal',
#    },
}

# Legacy name retained as an alias for any local user edits / old references.
EMPIRICAL_LAYOUTS = INSTRUMENT_LAYOUTS['CM']

INSTRUMENT_LABELS = {
    'CM': 'CM / ColorMunki',
    'i1': 'i1 / i1Pro',
    '3p': '3p / i1Pro3+',
#    'SS': 'SS / SpectroScan',
}

# Less common Argyll instrument codes retained here for users who want to add
# them back into the selector list later:
# INSTRUMENT_CODES_EXTRA = ['20', '22', '41', '51']


def normalise_instrument_code(instrument):
    """Return a canonical instrument code for layout-table lookups."""
    inst = str(instrument or 'CM').strip()
    if not inst:
        return 'CM'
    for known in INSTRUMENT_LAYOUTS.keys():
        if inst.lower() == known.lower():
            return known
    return inst


def instrument_layouts_for(instrument):
    """Return the layout table for an instrument, or an empty table if unknown."""
    return INSTRUMENT_LAYOUTS.get(normalise_instrument_code(instrument), {})


def instrument_label(instrument):
    """Return a readable instrument label for popup headings and logs."""
    inst = normalise_instrument_code(instrument)
    return INSTRUMENT_LABELS.get(inst, inst or 'custom instrument')


def patch_layout_note(patches, paper_size=None, instrument='CM'):
    """Return empirically mapped YAAW target-layout guidance.

    This is display/logging text only; it does not alter printtarg command
    generation.

    Do not calculate layouts from paper area.  These mappings are explicit
    empirical relationships between the selected Instrument, selected Paper
    Size, and selected patch count.  Any combination not listed here is
    reported as custom, because its practical layout can only be confirmed by
    testing printtarg with that instrument, paper size, margins, labels, strip
    geometry, and instrument constraints.
    """
    patch_text = str(patches or '').strip()
    paper = str(paper_size or '').strip()
    inst = normalise_instrument_code(instrument)

    # Normalise legacy/internal paper-size spellings used by old saved configs.
    paper_aliases = {
        '420x297': 'A3R',
        '594x420': 'A2R',
    }
    paper = paper_aliases.get(paper, paper)

    table = instrument_layouts_for(inst)
    if (paper, patch_text) in table:
        return table[(paper, patch_text)]

    if not paper or paper == '—':
        return f'custom layout: select a paper size to show {instrument_label(inst)} guidance'

    if not table:
        return f'custom layout: no empirical table for instrument {inst}; test and add rows'

    return f'custom layout: no empirical mapping for {patch_text or "custom"} patches on {paper} with {inst}'



class PrinterProfilingGUI:
    """Main GUI application for printer profiling workflow"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Yet Another Argyll Wrapper - build v3.40.23")
        self._apply_plain_ttk_theme()
        
        # Configuration and working directory setup
        self.config_file = SESSION_FILE
        
        # Variables for form fields
        self.vars = {}
        self.demo_mode = False
        self.main_thread = threading.current_thread()
        self.run_log_file = None  # Persistent per-project log activated when a workflow step is run
        self._run_log_failed = False
        self._loading_config = False
        self._details_available = False
        self.argyll_bin_dir = None
        self.argyll_doc_dir = None
        self.argyll_install_root = None
        
        # Locate ArgyllCMS, update this process PATH if necessary, and retain
        # the associated documentation location for the Help buttons.
        if not self.check_dependencies():
            if self.ask_yes_no("Continue Anyway?", 
                "ArgyllCMS tools not found. Continue anyway?\n\n" +
                "Note: You can configure settings but won't be able to run profiling steps."):
                self.demo_mode = True
                self.root.title("YAAW Printer Profiling Tool (DEMO MODE - ArgyllCMS not installed)")
            else:
                self.root.destroy()
                return
        
        # Try to load previous session before creating widgets
        self.loaded_session = self.try_load_session_data()
        
        # Create GUI
        self.create_widgets()
        self._autosize_window()
        
        # Handle session restore based on whether meaningful progress was made
        if self.loaded_session:
            last_step = self.loaded_session.get('last_step_completed', 0)
            if last_step >= 1:
                # Meaningful progress exists — ask the user whether to resume
                timestamp = self.loaded_session.get('timestamp', 'unknown time')
                try:
                    dt = datetime.fromisoformat(timestamp)
                    timestamp = dt.strftime('%Y-%m-%d %H:%M')
                except Exception:
                    pass
                resume = self.ask_yes_no(
                    "Resume Auto-Recovery Session?",
                    f"An auto-recovery session was found.\n\n"
                    f"Recovery file:\n{self.config_file}\n\n"
                    f"Last completed workflow step: {last_step}\n"
                    f"Last saved: {timestamp}\n\n"
                    "This is the transient crash-recovery session that is saved while you type; "
                    "it is not necessarily a project JSON saved beside the Argyll files.\n\n"
                    "Would you like to restore this recovery session?"
                )
                if resume:
                    self.apply_loaded_session()
                    self.log(f"Auto-recovery session restored from {self.config_file} (Step {last_step} previously completed on {timestamp}).")
                else:
                    try:
                        self.config_file.unlink()
                    except Exception:
                        pass
                    self.log("Auto-recovery session discarded. Starting fresh session.")
            # If last_step == 0 (no meaningful progress), start with defaults silently
    
    def _apply_plain_ttk_theme(self):
        """Apply YAAW's restrained, standard-library-only visual styling.

        The built-in clam theme remains the portable base.  A small neutral
        palette, clearer typography, and one muted accent improve readability
        without external themes, image assets, or platform-specific code.
        """
        try:
            style = ttk.Style()
            if "clam" in style.theme_names():
                style.theme_use("clam")

            self._yaaw_bg = "#f3f3f3"
            self._yaaw_text = "#303030"
            self._yaaw_hint = "#555555"
            self._yaaw_accent = "#365f7d"
            self._yaaw_accent_active = "#467594"
            self._yaaw_accent_pressed = "#294b64"
            self._yaaw_output_bg = "#fafafa"

            self.root.configure(background=self._yaaw_bg)
            style.configure(".", background=self._yaaw_bg, foreground=self._yaaw_text)
            style.configure("TFrame", background=self._yaaw_bg)
            style.configure("TLabel", background=self._yaaw_bg, foreground=self._yaaw_text)
            style.configure("TLabelframe", background=self._yaaw_bg)
            style.configure(
                "TLabelframe.Label",
                background=self._yaaw_bg,
                foreground=self._yaaw_text,
                font=("TkDefaultFont", 10, "bold"),
            )
            style.configure("TNotebook", background=self._yaaw_bg)

            # Emphasise only navigation, screen-edge actions, and main workflow
            # controls.  Keep the platform's normal interface font size.
            import tkinter.font as tkfont
            default_font = tkfont.nametofont("TkDefaultFont")
            try:
                self._yaaw_button_font = tkfont.Font(
                    root=self.root,
                    name="YAAWButtonFont",
                    exists=True,
                )
            except tk.TclError:
                self._yaaw_button_font = tkfont.Font(
                    root=self.root,
                    name="YAAWButtonFont",
                )
            self._yaaw_button_font.configure(**default_font.actual())
            self._yaaw_button_font.configure(weight="bold")

            style.configure("YAAWHeader.TButton", font="YAAWButtonFont")
            style.configure("YAAWHeader.Toolbutton", font="YAAWButtonFont")
            style.configure("YAAWAction.TButton", font="YAAWButtonFont")
            style.configure(
                "YAAWPrimary.TButton",
                font="YAAWButtonFont",
                foreground="white",
                background=self._yaaw_accent,
            )
            style.map(
                "YAAWPrimary.TButton",
                foreground=[("disabled", "#dddddd"), ("!disabled", "white")],
                background=[
                    ("pressed", self._yaaw_accent_pressed),
                    ("active", self._yaaw_accent_active),
                    ("disabled", "#8c9aa3"),
                ],
            )
        except Exception:
            pass

    def get_working_dir(self):
        """Get the working directory for the current job.

        Once the GUI has created the working_dir variable, honour that field
        directly.  Before then, fall back to WORKING_ROOT/basename.
        """
        working_var = self.vars.get('working_dir')
        if working_var is not None:
            value = working_var.get().strip()
            if value:
                return Path(os.path.expanduser(value))

        basename = self.vars.get('basename', tk.StringVar()).get().strip()
        if basename:
            dir_name = strip_argyll_suffix(basename)
            return WORKING_ROOT / dir_name
        return WORKING_ROOT

    @staticmethod
    def _argyll_version_key(path):
        """Return a sortable key for an Argyll_Vx.y.z installation path."""
        version = ()
        for part in Path(path).parts:
            match = re.fullmatch(r'Argyll_V(\d+(?:\.\d+)*)', part, re.IGNORECASE)
            if match:
                version = tuple(int(value) for value in match.group(1).split('.'))
                break
        try:
            modified = Path(path).stat().st_mtime
        except OSError:
            modified = 0
        return version, modified, str(path)

    def _argyll_candidate_bin_dirs(self):
        """Return a bounded list of likely ArgyllCMS bin directories.

        This deliberately avoids a full filesystem crawl.  It covers normal
        repository installs through PATH plus common upstream-archive layouts,
        including ~/Argyll/Argyll_V3.5.0/bin.
        """
        candidates = []

        def add(path):
            try:
                candidate = Path(path).expanduser()
                if candidate.is_dir():
                    resolved = candidate.resolve()
                    if resolved not in candidates:
                        candidates.append(resolved)
            except (OSError, RuntimeError):
                pass

        # First retain any directories already represented in PATH.
        for directory in os.environ.get('PATH', '').split(os.pathsep):
            if directory:
                add(directory)

        fixed = (
            Path('/usr/bin'),
            Path('/usr/local/bin'),
            Path('~/bin').expanduser(),
            Path('~/.local/bin').expanduser(),
        )
        for directory in fixed:
            add(directory)

        search_roots = (
            Path('~/Argyll').expanduser(),
            Path('~').expanduser(),
            Path('~/bin').expanduser(),
            Path('~/.local').expanduser(),
            Path('/opt'),
            Path('/usr/local'),
        )
        patterns = (
            'Argyll_V*/bin',
            'argyll_v*/bin',
            'argyll*/bin',
            '*/Argyll_V*/bin',
            '*/argyll_v*/bin',
        )
        discovered = []
        for root in search_roots:
            if not root.is_dir():
                continue
            for pattern in patterns:
                try:
                    discovered.extend(path for path in root.glob(pattern) if path.is_dir())
                except OSError:
                    pass

        # Newest version first when several unpacked releases coexist.
        for directory in sorted(set(discovered), key=self._argyll_version_key, reverse=True):
            add(directory)
        return candidates

    def _set_argyll_installation(self, bin_dir):
        """Record a discovered installation and prepend its bin dir to PATH."""
        bin_dir = Path(bin_dir).expanduser().resolve()
        self.argyll_bin_dir = bin_dir
        self.argyll_install_root = bin_dir.parent

        path_entries = [entry for entry in os.environ.get('PATH', '').split(os.pathsep) if entry]
        bin_text = str(bin_dir)
        if bin_text not in path_entries:
            os.environ['PATH'] = os.pathsep.join([bin_text] + path_entries)

        doc_dir = self.argyll_install_root / 'doc'
        self.argyll_doc_dir = doc_dir if doc_dir.is_dir() else None

    def check_dependencies(self):
        """Locate a complete ArgyllCMS toolset and configure it for YAAW."""
        required = ('targen', 'printtarg', 'chartread', 'colprof', 'profcheck')

        # Prefer the current PATH when it already exposes the complete suite.
        path_tools = {command: shutil.which(command) for command in required}
        if all(path_tools.values()):
            resolved_dirs = {
                Path(tool).expanduser().resolve().parent for tool in path_tools.values()
            }
            if len(resolved_dirs) == 1:
                self._set_argyll_installation(next(iter(resolved_dirs)))
            else:
                # Mixed repository layouts are valid; commands remain available,
                # but no single upstream doc tree can safely be inferred.
                self.argyll_bin_dir = None
                self.argyll_install_root = None
                self.argyll_doc_dir = None
            return True

        # Otherwise find one directory containing the complete suite.  Once
        # found, prepend it to this process PATH so every subprocess call and
        # shutil.which() lookup works normally for the rest of the session.
        for bin_dir in self._argyll_candidate_bin_dirs():
            if all((bin_dir / command).is_file() and os.access(bin_dir / command, os.X_OK)
                   for command in required):
                self._set_argyll_installation(bin_dir)
                return True

        missing = [command for command in required if shutil.which(command) is None]
        error_msg = (
            f"Missing ArgyllCMS tools: {', '.join(missing or required)}\n\n"
            "YAAW checked the current PATH and common manual-install locations, including:\n"
            "  ~/Argyll/Argyll_V*/bin\n"
            "  ~/Argyll_V*/bin\n"
            "  ~/bin and ~/.local\n"
            "  /opt and /usr/local\n\n"
            "Please install ArgyllCMS or unpack the official archive into one of those locations.\n\n"
            "Ubuntu/Debian repository package:\n"
            "  sudo apt install argyll\n\n"
            "Manual installation:\n"
            "  Download from https://www.argyllcms.com/ and retain the bin and doc directories together."
        )
        self.show_error('Missing Dependencies', error_msg)
        return False

    def _autosize_window(self):
        """Size the startup window conservatively, capped at screen size.

        Earlier 3.39 builds used Tk's requested width for the whole widget
        tree.  That request includes every long hint label and wide grid row,
        so on large monitors Tk could ask for a very wide window and YAAW
        would obediently open at roughly 80% of a 4K screen.

        KISS behaviour: start at a comfortable fixed width, allow a modest
        expansion for platform/theme differences, but do not scale the startup
        width with monitor size.  The user can still resize/maximise manually.
        """
        self.root.update_idletasks()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        # Measure the full scrollable content height via the canvas scrollregion.
        canvas = self._config_canvas
        canvas.update_idletasks()
        bbox = canvas.bbox("all")
        if bbox:
            content_h = bbox[3] - bbox[1]
        else:
            content_h = 900

        # Add header row, notebook padding, outer padding, and title bar.
        requested_h = self.root.winfo_reqheight()
        win_h = min(max(content_h + 95, requested_h), screen_h - 60)

        # Keep startup width screen-independent.  Do not use winfo_reqwidth()
        # directly here: the requested width is inflated by long explanatory
        # labels and therefore grows with available display space/theme metrics.
        preferred_w = 1440
        minimum_w = 1200
        max_startup_w = min(1500, screen_w - 80)
        win_w = max(minimum_w, min(preferred_w, max_startup_w))

        self.root.geometry(f"{win_w}x{win_h}")

    def create_widgets(self):
        """Create the GUI layout.

        Keep the tab selectors and project-level Save/Load actions on one
        visible top row.  ttk.Notebook does not support arbitrary widgets in
        its native tab strip, so YAAW uses a small header row with simple
        tab-selector buttons on the left and Save/Load on the right, while the
        notebook itself holds the pages below.  This avoids platform-specific
        theme hacks and keeps the layout portable across Linux/*nix and macOS.
        """
        outer = ttk.Frame(self.root)
        outer.pack(fill='both', expand=True, padx=10, pady=10)

        header = ttk.Frame(outer)
        header.pack(fill='x', pady=(0, 4))

        tab_frame = ttk.Frame(header)
        tab_frame.pack(side='left')

        action_frame = ttk.Frame(header)
        action_frame.pack(side='right')
        ttk.Button(action_frame, text="Load Config", command=self.load_config, style="YAAWHeader.TButton").pack(side='left', padx=(0, 5))
        ttk.Button(action_frame, text="Save Config", command=self.save_config, style="YAAWHeader.TButton").pack(side='left', padx=(0, 5))
        ttk.Button(action_frame, text="Exit", command=self.root.destroy, style="YAAWHeader.TButton").pack(side='left')

        try:
            style = ttk.Style()
            style.layout('Tabless.TNotebook.Tab', [])
        except Exception:
            pass

        notebook = ttk.Notebook(outer, style='Tabless.TNotebook')
        notebook.pack(fill='both', expand=True)
        self.notebook = notebook

        self._tab_names = ['config', 'exec', 'about']
        self._tab_var = tk.StringVar(value='config')
        for key, label in zip(self._tab_names, ['Configuration', 'Execution', 'About']):
            ttk.Radiobutton(
                tab_frame,
                text=label,
                value=key,
                variable=self._tab_var,
                command=lambda k=key: self._select_tab(k),
                style='YAAWHeader.Toolbutton'
            ).pack(side='left', padx=(0, 4))

        # Create tabs
        config_frame = ttk.Frame(notebook, padding="10")
        exec_frame = ttk.Frame(notebook, padding="10")
        about_frame = ttk.Frame(notebook, padding="10")

        notebook.add(config_frame, text="Configuration")
        notebook.add(exec_frame, text="Execution")
        notebook.add(about_frame, text="About")
        notebook.bind('<<NotebookTabChanged>>', self._sync_tab_selector, add='+')

        self.create_config_tab(config_frame)
        self.create_exec_tab(exec_frame)
        self.create_about_tab(about_frame)

    def _select_tab(self, key):
        """Select a notebook page from the header-row tab buttons."""
        try:
            index = self._tab_names.index(key)
            self.notebook.select(index)
        except Exception:
            pass

    def _sync_tab_selector(self, event=None):
        """Keep the header-row tab buttons in sync with notebook changes."""
        try:
            index = self.notebook.index(self.notebook.select())
            self._tab_var.set(self._tab_names[index])
        except Exception:
            pass

    def create_config_tab(self, parent):
        """Create configuration form with all profiling settings"""
        # Scrollable frame setup
        canvas = tk.Canvas(parent, background=self._yaaw_bg, highlightthickness=0)
        self._config_canvas = canvas
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Keep the configuration page fitted to the visible canvas width.
        # Without this, the page adopts the natural width of its longest hint
        # labels, placing right-aligned controls (such as the top Instrument
        # selector) beyond the visible edge even when the main window is wide.
        def _fit_config_page_to_canvas(event):
            try:
                canvas.itemconfigure(canvas_window, width=event.width)
            except Exception:
                pass

        canvas.bind('<Configure>', _fit_config_page_to_canvas, add='+')

        # The printtarg instrument affects target layout, generated names, and
        # chartread's -H default.  Put a linked selector at the very top so it
        # is the first setting the user sees.  Both this selector and the one
        # in printtarg Settings share the same StringVar, so changing either
        # immediately changes the other.
        self.vars['printtarg_instrument'] = tk.StringVar(value="CM")

        # === Basic Information Section ===
        basic_outer = ttk.Frame(scrollable_frame)
        basic_outer.pack(fill='x', padx=5, pady=5)

        basic_header = ttk.Frame(basic_outer)
        basic_header.pack(fill='x', padx=8, pady=(0, 2))
        ttk.Label(
            basic_header,
            text="Basic Information",
            font=('TkDefaultFont', 10, 'bold')
        ).pack(side='left')

        top_instr_frame = ttk.Frame(basic_header)
        top_instr_frame.pack(side='right')
        ttk.Label(top_instr_frame, text="Instrument:", font=('TkDefaultFont', 10, 'bold')).pack(side='left', padx=(0, 5))
        top_instr_combo = ttk.Combobox(
            top_instr_frame,
            textvariable=self.vars['printtarg_instrument'],
            values=['CM', 'i1', '3p'],
            width=10,
            state='normal'
        )
        self.top_instrument_combo = top_instr_combo
        top_instr_combo.pack(side='left')
        top_instr_combo.bind('<<ComboboxSelected>>', lambda e: self._on_instrument_changed(), add='+')
        top_instr_combo.bind('<FocusOut>', lambda e: self._on_instrument_changed(), add='+')

        section = ttk.LabelFrame(basic_outer, text="", padding="10")
        section.pack(fill='x')
        
        self.create_field(section, "printer_name", "Printer Name:", "", 
            "Printer Name or Model")
        self.create_field(section, "paper_name", "Paper Name:", "",
            "Type of paper being profiled")
        self.create_field(section, "ink_name", "Ink Type:", "",
            "Ink type (OEM, Third-party brand, etc.)")
        self.create_field(section, "profile_desc", "Profile Description:", "",
            "Full description (auto-filled from above & Patches)",
            width=50)
        self.create_field(section, "basename", "Base Filename:", "",
            "Base name for output files (auto-filled)",
            width=50)
        
        # === Output Settings Section ===
        section = ttk.LabelFrame(scrollable_frame, text="Output Settings", padding="10")
        section.pack(fill='x', padx=6, pady=(4, 8))

        # Working Directory
        working_frame = ttk.Frame(section)
        working_frame.pack(fill='x', pady=2)
        ttk.Label(working_frame, text="Working Directory:", width=25).pack(side='left')
        default_working = str(WORKING_ROOT)
        self.vars['working_dir'] = tk.StringVar(value=default_working)
        working_entry = ttk.Entry(working_frame, textvariable=self.vars['working_dir'], width=40)
        working_entry.pack(side='left', padx=5)
        browse_working_btn = ttk.Button(working_frame, text="Browse...", command=self.browse_working_dir)
        browse_working_btn.pack(side='left', padx=5)
        ttk.Label(working_frame, text="Intermediate files (ti1, ti3, etc.)",
                  foreground='#555555', font=('TkDefaultFont', 9)).pack(side='left', padx=5)

        output_frame = ttk.Frame(section)
        output_frame.pack(fill='x', pady=2)
        ttk.Label(output_frame, text="Output Directory:", width=25).pack(side='left')
        default_output = str(ICC_OUTPUT_ROOT)
        self.vars['output_dir'] = tk.StringVar(value=default_output)
        output_entry = ttk.Entry(output_frame, textvariable=self.vars['output_dir'], width=40)
        output_entry.pack(side='left', padx=5)
        browse_btn = ttk.Button(output_frame, text="Browse...", command=self.browse_output_dir)
        browse_btn.pack(side='left', padx=5)

        # === targen Settings Section ===
        section = ttk.LabelFrame(scrollable_frame, text="targen Settings", padding="10")
        section.pack(fill='x', padx=6, pady=(4, 8))

        # 3x3 grid — labels in cols 0,3,6 / widgets in cols 1,4,7 / hints in cols 2,5,8
        grid_frame = ttk.Frame(section)
        grid_frame.pack(fill='x', pady=4)

        # Fixed label width ensures all four columns align regardless of text length
        LBL_W = 14

        def grid_label(row, col, text):
            ttk.Label(grid_frame, text=text, width=LBL_W, anchor='w').grid(
                row=row, column=col, sticky='w', padx=(0, 2), pady=3)

        def grid_hint(row, col, text):
            ttk.Label(grid_frame, text=text, foreground='gray',
                      font=('TkDefaultFont', 8)).grid(
                row=row, column=col, sticky='w', padx=(2, 10), pady=3)

        def grid_entry(row, col, var_name, default):
            self.vars[var_name] = tk.StringVar(value=default)
            ttk.Entry(grid_frame, textvariable=self.vars[var_name], width=6).grid(
                row=row, column=col, sticky='w', padx=(0, 2), pady=3)

        def grid_combo(row, col, var_name, default, values, state='readonly'):
            self.vars[var_name] = tk.StringVar(value=default)
            combo = ttk.Combobox(grid_frame, textvariable=self.vars[var_name],
                                 values=values, width=6, state=state)
            combo.grid(row=row, column=col, sticky='w', padx=(0, 2), pady=3)
            return combo

        # Row 0: Patches, Ink Limit, Grey Steps, Neutral Steps
        grid_label(0, 0, "Patches:")
        # Keep the visible Patches control the same compact combobox style as
        # the other selector fields.  Clicking its drop-down arrow opens YAAW's
        # annotated empirical-layout selector instead of a long native list, so
        # explanatory text never stretches the targen settings grid.
        self.vars['patches'] = tk.StringVar(value='460')
        patch_values = self._patch_values_for_current_instrument()
        self.patches_combo = ttk.Combobox(
            grid_frame,
            textvariable=self.vars['patches'],
            values=patch_values,
            width=6,
            state='normal'
        )
        self.patches_combo.grid(row=0, column=1, sticky='w', padx=(0, 2), pady=3)
        self.patches_combo.bind('<Button-1>', self._on_patches_combo_click, add='+')
        self.patches_combo.bind('<Alt-Down>', lambda e: (self.show_patch_layout_selector(), 'break')[1], add='+')
        self.patches_combo.bind('<F4>', lambda e: (self.show_patch_layout_selector(), 'break')[1], add='+')
        grid_hint(0, 2, "(-f)")
        grid_label(0, 3, "Ink Limit:");        grid_entry(0, 4, 'ink_limit',              '300'); grid_hint(0, 5, "(-l)")
        grid_label(0, 6, "Grey Steps:");       grid_entry(0, 7, 'targen_grey_steps',       '16'); grid_hint(0, 8, "(-g)")
        grid_label(0, 9, "Neutral Steps:");    grid_entry(0, 10, 'targen_neutral_steps',    '8'); grid_hint(0, 11, "(-n)")

        # Row 1: Neutral Emphasis, Dark Emphasis, White Patches, Black Patches
        grid_label(1, 0, "Neut. Emphasis:"); grid_entry(1, 1, 'targen_neutral_emphasis', '0.5'); grid_hint(1, 2, "(-N)")
        grid_label(1, 3, "Dark Emphasis:");  grid_entry(1, 4, 'targen_dark_emphasis',    '1.0'); grid_hint(1, 5, "(-V)")
        grid_label(1, 6, "White Patches:");  grid_entry(1, 7, 'targen_white_patches',      '4'); grid_hint(1, 8, "(-e)")
        grid_label(1, 9, "Black Patches:");  grid_entry(1, 10, 'targen_black_patches',     '4'); grid_hint(1, 11, "(-B)")

        # Preconditioning profile at the bottom of the section
        precond_frame = ttk.Frame(section)
        precond_frame.pack(fill='x', pady=(8, 2))
        ttk.Label(precond_frame, text="Preconditioning Profile:", width=25).pack(side='left')
        self.vars['precond_profile'] = tk.StringVar(value="")
        precond_entry = ttk.Entry(precond_frame, textvariable=self.vars['precond_profile'], width=60)
        precond_entry.pack(side='left', padx=5)
        self.vars['precond_profile'].trace_add('write', lambda *a: precond_entry.after(10, lambda: precond_entry.xview_moveto(1)))
        ttk.Button(precond_frame, text="Browse...", command=self.browse_precond_profile).pack(side='left', padx=5)
        ttk.Label(precond_frame, text="(-c)  Empty: Argyll default; 'none': disabled",
                  foreground='#555555', font=('TkDefaultFont', 9)).pack(side='left', padx=5)

        targen_extra_frame = ttk.Frame(section)
        targen_extra_frame.pack(fill='x', pady=2)
        ttk.Label(targen_extra_frame, text="Additional targen Args:", width=25).pack(side='left')
        self.vars['targen_extra_args'] = tk.StringVar(value="")
        ttk.Entry(targen_extra_frame, textvariable=self.vars['targen_extra_args'], width=32).pack(side='left', padx=5)
        ttk.Button(targen_extra_frame, text="Help: targen", width=14,
                   command=lambda: self.open_man_page("targen")).pack(side='right', padx=5)

        # === printtarg Settings Section ===
        section = ttk.LabelFrame(scrollable_frame, text="printtarg Settings", padding="10")
        section.pack(fill='x', padx=6, pady=(4, 8))

        # Instrument (-i)
        instr_frame = ttk.Frame(section)
        instr_frame.pack(fill='x', pady=2)
        ttk.Label(instr_frame, text="Instrument:", width=25).pack(side='left')
        instr_combo = ttk.Combobox(instr_frame, textvariable=self.vars['printtarg_instrument'],
                                   values=['CM', 'i1', '3p'],
 #                                  values=['CM', 'i1', '3p', 'SS', '20', '22', '41', '51'],
                                   width=10, state='normal')
        self.instrument_combo = instr_combo
        instr_combo.pack(side='left', padx=5)
        instr_combo.bind('<<ComboboxSelected>>', lambda e: self._on_instrument_changed(), add='+')
        instr_combo.bind('<FocusOut>', lambda e: self._on_instrument_changed(), add='+')
        ttk.Label(instr_frame, text="(-i)  CM=ColorMunki (default), i1=i1Pro, 3p=i1Pro3+; other Argyll codes may be typed manually",
                  foreground='#555555', font=('TkDefaultFont', 9)).pack(side='left', padx=5)

        # Output Image Type (no flag=PS / -e=EPS / -t=TIFF 8bit / -T=TIFF 16bit)
        imgtype_frame = ttk.Frame(section)
        imgtype_frame.pack(fill='x', pady=2)
        ttk.Label(imgtype_frame, text="Output Image Type:", width=25).pack(side='left')
        self.vars['printtarg_imgtype'] = tk.StringVar(value="PS (Postscript)")
        imgtype_combo = ttk.Combobox(imgtype_frame, textvariable=self.vars['printtarg_imgtype'],
                                     values=['PS (Postscript)', 'EPS (-e)', 'TIFF 8-bit (-t 300)', 'TIFF 16-bit (-T 300)'],
                                     width=22, state='readonly')
        imgtype_combo.pack(side='left', padx=5)
        ttk.Label(imgtype_frame, text="Default: TIFF 16-bit (-T 300)",
                  foreground='#555555', font=('TkDefaultFont', 9)).pack(side='left', padx=5)

        # Hexagon/DD Patches (-h)
        hex_frame = ttk.Frame(section)
        hex_frame.pack(fill='x', pady=2)
        ttk.Label(hex_frame, text="Hexagon/DD Patches:", width=25).pack(side='left')
        self.vars['printtarg_hexagon'] = tk.BooleanVar(value=True)
        ttk.Checkbutton(hex_frame, variable=self.vars['printtarg_hexagon']).pack(side='left', padx=5)
        ttk.Label(hex_frame, text="(-h)  Default: Selected",
                  foreground='#555555', font=('TkDefaultFont', 9)).pack(side='left', padx=5)

        # Paper Size (-p)
        papersize_frame = ttk.Frame(section)
        papersize_frame.pack(fill='x', pady=2)
        ttk.Label(papersize_frame, text="Paper Size:", width=25).pack(side='left')
        self.vars['paper_size'] = tk.StringVar(value="A3")
        papersize_combo = ttk.Combobox(papersize_frame, textvariable=self.vars['paper_size'],
                                       values=['4x6', 'A4', 'A4R', 'A3', 'A3R', 'A2', 'A2R', 'Letter', 'LetterR', '11x17'],
                                       width=10, state='normal')
        self.papersize_combo = papersize_combo
        papersize_combo.pack(side='left', padx=5)
        ttk.Label(papersize_frame, text="(-p)  Named size or custom WWWxHHH mm; A3R=420x297, A2R=594x420",
                  foreground='#555555', font=('TkDefaultFont', 9)).pack(side='left', padx=5)

        printtarg_extra_frame = ttk.Frame(section)
        printtarg_extra_frame.pack(fill='x', pady=2)
        ttk.Label(printtarg_extra_frame, text="Additional printtarg Args:", width=25).pack(side='left')
        self.vars['printtarg_extra_args'] = tk.StringVar(value="")
        ttk.Entry(printtarg_extra_frame, textvariable=self.vars['printtarg_extra_args'], width=32).pack(side='left', padx=5)
        ttk.Button(printtarg_extra_frame, text="Help: printtarg", width=14,
                   command=lambda: self.open_man_page("printtarg")).pack(side='right', padx=5)

        # === chartread Settings Section ===
        section = ttk.LabelFrame(scrollable_frame, text="chartread Settings", padding="10")
        section.pack(fill='x', padx=6, pady=(4, 8))

        # Patch Consistence Threshold (-T)
        pct_frame = ttk.Frame(section)
        pct_frame.pack(fill='x', pady=2)
        ttk.Label(pct_frame, text="Patch Consistence\nThreshold:", width=25).pack(side='left')
        self.vars['chartread_threshold'] = tk.StringVar(value="1")
        ttk.Entry(pct_frame, textvariable=self.vars['chartread_threshold'], width=10).pack(side='left', padx=5)
        ttk.Label(pct_frame, text="(-T)  Default: 1",
                  foreground='#555555', font=('TkDefaultFont', 9)).pack(side='left', padx=5)

        # Save CIE as XYZ / Lab / Both
        cie_frame = ttk.Frame(section)
        cie_frame.pack(fill='x', pady=2)
        ttk.Label(cie_frame, text="Save CIE as:", width=25).pack(side='left')
        self.vars['chartread_cie'] = tk.StringVar(value="Lab (-l)")
        cie_combo = ttk.Combobox(cie_frame, textvariable=self.vars['chartread_cie'],
                                 values=['XYZ (default)', 'Lab (-l)', 'Both XYZ+Lab (-L)'],
                                 width=20, state='readonly')
        cie_combo.pack(side='left', padx=5)
        ttk.Label(cie_frame, text="Default: Lab (-l)",
                  foreground='#555555', font=('TkDefaultFont', 9)).pack(side='left', padx=5)

        # chartread operating modes.  Keep the established -H/-S controls in
        # the left column; place -r beside -H and -p directly below it.
        chartread_modes = ttk.Frame(section)
        chartread_modes.pack(fill='x', pady=2)

        self.vars['chartread_highres'] = tk.BooleanVar(value=True)
        self.vars['chartread_resume'] = tk.BooleanVar(value=False)
        self.vars['chartread_supwrn'] = tk.BooleanVar(value=False)
        self.vars['chartread_patch_by_patch'] = tk.BooleanVar(value=False)

        ttk.Label(chartread_modes, text="High Resolution Spectrum:", width=25).grid(
            row=0, column=0, sticky='w', pady=2)
        ttk.Checkbutton(chartread_modes, variable=self.vars['chartread_highres']).grid(
            row=0, column=1, sticky='w', padx=5, pady=2)
        ttk.Label(chartread_modes, text="(-H)  Default ON for CM, OFF for i1/3p",
                  foreground='#555555', font=('TkDefaultFont', 9)).grid(
            row=0, column=2, sticky='w', padx=(0, 24), pady=2)

        ttk.Label(chartread_modes, text="Resume Partly Read Chart:", width=24).grid(
            row=0, column=3, sticky='w', pady=2)
        ttk.Checkbutton(chartread_modes, variable=self.vars['chartread_resume']).grid(
            row=0, column=4, sticky='w', padx=5, pady=2)
        ttk.Label(chartread_modes, text="(-r)  Re-read or resume partly read chart", foreground='#555555',
                  font=('TkDefaultFont', 9)).grid(row=0, column=5, sticky='w', pady=2)

        ttk.Label(chartread_modes, text="Suppress Warnings:", width=25).grid(
            row=1, column=0, sticky='w', pady=2)
        ttk.Checkbutton(chartread_modes, variable=self.vars['chartread_supwrn']).grid(
            row=1, column=1, sticky='w', padx=5, pady=2)
        ttk.Label(chartread_modes, text="(-S)  Suppress wrong strip & unexpected value warnings",
                  foreground='#555555', font=('TkDefaultFont', 9)).grid(
            row=1, column=2, sticky='w', padx=(0, 24), pady=2)

        ttk.Label(chartread_modes, text="Read Patch By Patch:", width=24).grid(
            row=1, column=3, sticky='w', pady=2)
        ttk.Checkbutton(chartread_modes, variable=self.vars['chartread_patch_by_patch']).grid(
            row=1, column=4, sticky='w', padx=5, pady=2)
        ttk.Label(chartread_modes, text="(-p)  Measure Patch by Patch rather than Strip", foreground='#555555',
                  font=('TkDefaultFont', 9)).grid(row=1, column=5, sticky='w', pady=2)

        chartread_extra_frame = ttk.Frame(section)
        chartread_extra_frame.pack(fill='x', pady=2)
        ttk.Label(chartread_extra_frame, text="Additional chartread Args:", width=25).pack(side='left')
        self.vars['chartread_extra_args'] = tk.StringVar(value="")
        ttk.Entry(chartread_extra_frame, textvariable=self.vars['chartread_extra_args'], width=32).pack(side='left', padx=5)
        ttk.Button(chartread_extra_frame, text="Help: chartread", width=14,
                   command=lambda: self.open_man_page("chartread")).pack(side='right', padx=5)

        # === colprof Settings Section ===
        section = ttk.LabelFrame(scrollable_frame, text="colprof Settings", padding="10")
        section.pack(fill='x', padx=6, pady=(4, 8))

        # Rendering profile selection
        self.create_field(section, "colprof_description", "Description:", "", "-D  Profile description string", width=60)
        source_frame = ttk.Frame(section)
        source_frame.pack(fill='x', pady=2)
        ttk.Label(source_frame, text="Rendering Profile:", width=25).pack(side='left')
        self.vars['rendering_profile'] = tk.StringVar(value="")
        source_entry = ttk.Entry(source_frame, textvariable=self.vars['rendering_profile'], width=60)
        source_entry.pack(side='left', padx=5)
        self.vars['rendering_profile'].trace_add('write', lambda *a: source_entry.after(10, lambda: source_entry.xview_moveto(1)))
        browse_source_btn = ttk.Button(source_frame, text="Browse...", command=self.browse_rendering_profile)
        browse_source_btn.pack(side='left', padx=5)
        ttk.Label(source_frame, text="(-S)  ICC profile for rendering intent source gamut",
                  foreground='#555555', font=('TkDefaultFont', 9)).pack(side='left', padx=5)

        # Default Rendering Intent (-Z)
        intent_frame = ttk.Frame(section)
        intent_frame.pack(fill='x', pady=2)
        ttk.Label(intent_frame, text="Default Rendering Intent:", width=25).pack(side='left')
        self.vars['colprof_intent'] = tk.StringVar(value="r - Rel. Colorimetric")
        intent_combo = ttk.Combobox(intent_frame, textvariable=self.vars['colprof_intent'],
                                    values=['p - Perceptual', 'r - Rel. Colorimetric',
                                            's - Saturation', 'a - Abs. Colorimetric'],
                                    width=22, state='readonly')
        intent_combo.pack(side='left', padx=5)
        ttk.Label(intent_frame, text="(-Z)  Default: Rel. Colorimetric",
                  foreground='#555555', font=('TkDefaultFont', 9)).pack(side='left', padx=5)

        # Quality (-q)
        quality_frame = ttk.Frame(section)
        quality_frame.pack(fill='x', pady=2)
        ttk.Label(quality_frame, text="Quality:", width=25).pack(side='left')
        self.vars['colprof_quality'] = tk.StringVar(value="h - High")
        quality_combo = ttk.Combobox(quality_frame, textvariable=self.vars['colprof_quality'],
                                     values=['l - Low', 'm - Medium', 'h - High', 'u - Ultra (for testing only)'],
                                     width=22, state='readonly')
        quality_combo.pack(side='left', padx=5)
        ttk.Label(quality_frame, text="(-q)  Default: High",
                  foreground='#555555', font=('TkDefaultFont', 9)).pack(side='left', padx=5)

        # Average Deviation (-r)
        avgdev_frame = ttk.Frame(section)
        avgdev_frame.pack(fill='x', pady=2)
        ttk.Label(avgdev_frame, text="Average Deviation:", width=25).pack(side='left')
        self.vars['colprof_avgdev'] = tk.StringVar(value="0.5")
        ttk.Entry(avgdev_frame, textvariable=self.vars['colprof_avgdev'], width=10).pack(side='left', padx=5)
        ttk.Label(avgdev_frame, text="(-r)  Percentage, default 0.5%",
                  foreground='#555555', font=('TkDefaultFont', 9)).pack(side='left', padx=5)

        colprof_extra_frame = ttk.Frame(section)
        colprof_extra_frame.pack(fill='x', pady=2)
        ttk.Label(colprof_extra_frame, text="Additional colprof Args:", width=25).pack(side='left')
        self.vars['colprof_extra_args'] = tk.StringVar(value="")
        ttk.Entry(colprof_extra_frame, textvariable=self.vars['colprof_extra_args'], width=32).pack(side='left', padx=5)
        ttk.Button(colprof_extra_frame, text="Help: colprof", width=14,
                   command=lambda: self.open_man_page("colprof")).pack(side='right', padx=5)

        self.create_field(section, "colprof_manufacturer", "Manufacturer:", "",
            "-A  Manufacturer/vendor string")
        self.create_field(section, "colprof_model", "Model:", "",
            "-M  Model string")
        self.create_field(section, "colprof_copyright", "Copyright:", "",
            "-C  Copyright string")

        # === Project Overview Section ===
        self.create_project_overview(scrollable_frame)

        # Set up auto-fill handlers
        self.vars['printer_name'].trace_add('write', self._on_identity_field_changed)
        self.vars['paper_name'].trace_add('write', self._on_identity_field_changed)
        self.vars['ink_name'].trace_add('write', self._on_identity_field_changed)
        self.vars['patches'].trace_add('write', self._on_identity_field_changed)
        self.vars['printtarg_instrument'].trace_add('write', lambda *args: self._on_instrument_changed())
        self.vars['basename'].trace_add('write', lambda *args: (self._update_working_dir(), self._queue_visual_polish_refresh()))
        self.vars['profile_desc'].trace_add('write', lambda *args: (self._sync_colprof_description(), self._queue_visual_polish_refresh()))
        self._install_visual_polish_traces()
        
        # Pack scrollbar and canvas
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Run initial autofill with default values.  If a previous session is
        # later resumed, apply_loaded_session() recomputes these derived fields.
        self.autofill_fields()
    
    def _on_patches_combo_click(self, event):
        """Open the annotated layout selector when the combobox arrow is clicked.

        The Patches widget is an editable ttk.Combobox so it has the same
        native visual style as Instrument/Paper Size selectors.  YAAW intercepts
        clicks on the down-arrow element and shows the richer empirical-layout
        selector, because the native combobox drop-down is too narrow for the
        explanatory Paper/Patches guidance.
        """
        try:
            element = event.widget.identify(event.x, event.y)
        except Exception:
            element = ''
        if 'arrow' in str(element).lower() or 'down' in str(element).lower():
            self.show_patch_layout_selector()
            return 'break'
        return None

    def _current_instrument_code(self):
        """Return the current printtarg instrument code for layout selection."""
        var = self.vars.get('printtarg_instrument')
        return normalise_instrument_code(var.get() if var is not None else 'CM')

    def _chartread_highres_default_for_current_instrument(self):
        """Return YAAW's default chartread -H state for the current instrument.

        ColorMunki has been author-tested with -H.  i1/i1Pro and i1Pro3+
        user reports suggest -H can interfere with otherwise working
        chartread sessions, so leave it off by default for non-CM instruments.
        Users can still force -H via Additional chartread Args if needed.
        """
        return self._current_instrument_code() == 'CM'

    def _apply_chartread_highres_default(self):
        """Sync the High Resolution Spectrum checkbox with the instrument default."""
        var = self.vars.get('chartread_highres')
        if var is not None:
            try:
                var.set(self._chartread_highres_default_for_current_instrument())
            except Exception:
                pass

    def _layout_table_for_current_instrument(self):
        """Return the currently selected instrument's layout table."""
        return instrument_layouts_for(self._current_instrument_code())

    def _patch_values_for_current_instrument(self):
        """Return sorted patch counts for the current instrument's selector."""
        table = self._layout_table_for_current_instrument()
        if not table:
            table = INSTRUMENT_LAYOUTS['CM']
        values = {patches for (_paper, patches) in table.keys()}
        try:
            return sorted(values, key=lambda value: int(value))
        except Exception:
            return sorted(values)

    def _on_instrument_changed(self):
        """Refresh patch-layout guidance and generated names after Instrument changes."""
        try:
            if hasattr(self, 'patches_combo'):
                self.patches_combo.configure(values=self._patch_values_for_current_instrument())
        except Exception:
            pass
        if getattr(self, '_loading_config', False):
            return
        # Keep chartread's -H default conservative for i1/i1Pro and i1Pro3+.
        self._apply_chartread_highres_default()
        # Instrument is now part of the generated basename/profile description,
        # so changing it must update those derived fields just like changing
        # Printer/Paper/Ink/Patches.
        try:
            self.autofill_fields()
        except Exception:
            self._queue_visual_polish_refresh()

    def _empirical_layout_rows(self):
        """Return layout rows for the currently selected instrument."""
        paper_order = ['A4', 'A4R', 'A3', 'A3R', 'A2', 'A2R', 'Letter', '11x17']
        table = self._layout_table_for_current_instrument()
        rows = []
        for paper in paper_order:
            entries = [item for item in table.items() if item[0][0] == paper]
            entries.sort(key=lambda item: int(item[0][1]) if str(item[0][1]).isdigit() else 999999)
            for (paper_name, patches), note in entries:
                rows.append((paper_name, patches, note))
        if rows:
            return rows

        # Unknown manually-entered instrument: show a clear no-data row without
        # changing the user's current Patches/Paper values.
        current_patches = self.vars.get('patches', tk.StringVar(value='')).get().strip() or 'custom'
        current_paper = self.vars.get('paper_size', tk.StringVar(value='')).get().strip() or 'custom'
        inst = self._current_instrument_code()
        return [(current_paper, current_patches, f'No layout table for {inst}; test and add rows to INSTRUMENT_LAYOUTS')]

    def show_patch_layout_selector(self):
        """Show a transient annotated selector for empirical target layouts.

        The compact Patches field remains a plain editable count.  This popup
        is deliberately separate from the entry text so long explanatory layout
        descriptions do not stretch the targen settings grid.
        """
        if getattr(self, '_patch_layout_popup', None) is not None:
            try:
                if self._patch_layout_popup.winfo_exists():
                    self._patch_layout_popup.lift()
                    return
            except Exception:
                pass

        rows = self._empirical_layout_rows()
        popup = tk.Toplevel(self.root)
        self._patch_layout_popup = popup
        popup.title(f'Select target layout - {self._current_instrument_code()}')
        popup.transient(self.root)
        popup.resizable(True, True)

        outer = ttk.Frame(popup, padding=8)
        outer.pack(fill='both', expand=True)

        ttk.Label(
            outer,
            text=f'{instrument_label(self._current_instrument_code())} layout table. YAAW sets both Patches and Paper Size.',
            anchor='w'
        ).pack(fill='x', pady=(0, 6))

        table_frame = ttk.Frame(outer)
        table_frame.pack(fill='both', expand=True)

        columns = ('patches', 'paper', 'layout')

        # Some Linux desktops / themes use a larger Tk default font but leave
        # ttk.Treeview's default row height unchanged.  The result is the
        # clipped half-height rows shown on some high-DPI systems.  Give this
        # popup its own Treeview style and size rows from the actual font
        # metrics rather than relying on the theme default.
        try:
            import tkinter.font as tkfont
            default_font = tkfont.nametofont('TkDefaultFont')
            rowheight = max(24, default_font.metrics('linespace') + 10)
        except Exception:
            rowheight = 28
        try:
            style = ttk.Style(popup)
            style.configure('PatchLayout.Treeview', rowheight=rowheight)
        except Exception:
            pass

        visible_rows = min(16, len(rows))
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=visible_rows,
            style='PatchLayout.Treeview'
        )
        tree.heading('patches', text='Patches')
        tree.heading('paper', text='Paper')
        tree.heading('layout', text='Layout guidance')
        tree.column('patches', width=120, anchor='w', stretch=False)
        tree.column('paper', width=120, anchor='w', stretch=False)
        tree.column('layout', width=560, anchor='w', stretch=True)

        yscroll = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=yscroll.set)
        tree.pack(side='left', fill='both', expand=True)
        yscroll.pack(side='right', fill='y')

        for paper, patches, note in rows:
            tree.insert('', 'end', values=(patches, paper, note))

        def apply_selection(event=None):
            selected = tree.selection()
            if not selected:
                return
            patches, paper, note = tree.item(selected[0], 'values')
            self.vars['patches'].set(str(patches))
            self.vars['paper_size'].set(str(paper))
            self._queue_visual_polish_refresh()
            popup.destroy()

        button_row = ttk.Frame(outer)
        button_row.pack(fill='x', pady=(8, 0))
        ttk.Button(button_row, text='Cancel', command=popup.destroy).pack(side='right')
        ttk.Button(button_row, text='Use Selected Layout', command=apply_selection).pack(side='right', padx=(0, 6))

        tree.bind('<Double-1>', apply_selection)
        tree.bind('<Return>', apply_selection)
        popup.bind('<Escape>', lambda e: popup.destroy())
        popup.protocol('WM_DELETE_WINDOW', popup.destroy)
        popup.bind('<Destroy>', lambda e: setattr(self, '_patch_layout_popup', None) if e.widget is popup else None)

        # Size and position the popup after Tk has measured the themed widgets.
        # Keep it useful on large-font desktops while still fitting on smaller
        # screens, and avoid letting it extend beyond the right/bottom edge.
        try:
            popup.update_idletasks()
            widget = getattr(self, 'patches_combo', None) or self.root
            screen_w = popup.winfo_screenwidth()
            screen_h = popup.winfo_screenheight()
            desired_w = min(max(popup.winfo_reqwidth(), 840), max(520, screen_w - 80))
            desired_h = min(max(popup.winfo_reqheight(), 360), max(280, screen_h - 120))
            x = widget.winfo_rootx()
            y = widget.winfo_rooty() + widget.winfo_height() + 2
            if x + desired_w > screen_w - 40:
                x = max(20, screen_w - desired_w - 40)
            if y + desired_h > screen_h - 60:
                y = max(20, screen_h - desired_h - 60)
            popup.geometry(f'{desired_w}x{desired_h}+{x}+{y}')
            popup.minsize(min(520, desired_w), min(280, desired_h))
        except Exception:
            pass

        tree.focus_set()
        current_patches = self.vars.get('patches', tk.StringVar(value='')).get().strip()
        current_paper = self.vars.get('paper_size', tk.StringVar(value='')).get().strip()
        for item in tree.get_children(''):
            values = tree.item(item, 'values')
            if values and values[0] == current_patches and values[1] == current_paper:
                tree.selection_set(item)
                tree.see(item)
                break

    def create_project_overview(self, parent):
        """Create a compact, read-only project summary and file-status area.

        This isa only.  It does not alter filenames, paths,
        workflow state, or Argyll command generation.
        """
        overview_outer = ttk.LabelFrame(parent, text="Project Overview", padding="10")
        overview_outer.pack(fill='x', padx=5, pady=5)

        split = ttk.Frame(overview_outer)
        split.pack(fill='x')

        # Keep the two overview panels visually stable. If normal pack()
        # geometry is used here, the Summary panel can grow/shrink as its
        # content changes, which in turn squeezes the Files panel. Use a fixed
        # two-column grid with an approximately 2:1 Summary:Files width ratio.
        split.columnconfigure(0, weight=2, uniform='project_overview')
        split.columnconfigure(1, weight=1, uniform='project_overview')

        summary_frame = ttk.LabelFrame(split, text="Summary", padding="8")
        summary_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))

        files_frame = ttk.LabelFrame(split, text="Files", padding="8")
        files_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))

        self.project_summary_var = tk.StringVar(value="Project summary will appear once printer, paper, and ink are entered.")
        self.project_files_var = tk.StringVar(value="Project file status will appear once a basename is available.")

        # Fixed character widths keep requested widget sizes stable, while the
        # grid weights above set the visual 2:1 column split.
        ttk.Label(summary_frame, textvariable=self.project_summary_var, justify='left', anchor='nw', width=70).pack(fill='both', expand=True)
        ttk.Label(files_frame, textvariable=self.project_files_var, justify='left', anchor='nw', width=34).pack(fill='both', expand=True)

    def _on_identity_field_changed(self, *args):
        """Update derived identity fields and refresh the read-only overview."""
        if getattr(self, '_loading_config', False):
            return
        self.autofill_fields()
        self._queue_visual_polish_refresh()

    def _queue_visual_polish_refresh(self):
        """Refresh the overview after Tk has committed the latest field value.

        Some ttk widgets, especially editable comboboxes, can fire variable
        traces while related auto-fill traces are also running.  Scheduling the
        read-only overview update for idle time ensures the Expected layout
        line is calculated from the final current Patches value, not from a
        stale intermediate value.
        """
        try:
            self.root.after_idle(self._refresh_visual_polish)
        except Exception:
            self._refresh_visual_polish()

    def _install_visual_polish_traces(self):
        """Refresh read-only overview panels when relevant fields change."""
        watch = [
            'printer_name', 'paper_name', 'ink_name', 'profile_desc', 'basename',
            'patches', 'paper_size', 'printtarg_instrument', 'working_dir', 'output_dir', 'printtarg_imgtype'
        ]
        for name in watch:
            var = self.vars.get(name)
            if var is not None:
                try:
                    var.trace_add('write', lambda *args: self._queue_visual_polish_refresh())
                except Exception:
                    pass

        # Combobox traces should be enough, but bind the widgets too so mouse
        # selection, keyboard selection, typing in the editable Patches box,
        # and focus-out all refresh the read-only Expected layout line.
        for widget_name in ('patches_combo', 'papersize_combo', 'instrument_combo', 'top_instrument_combo'):
            widget = getattr(self, widget_name, None)
            if widget is not None:
                for event in ('<<ComboboxSelected>>', '<KeyRelease>', '<FocusOut>'):
                    try:
                        widget.bind(event, lambda e: self._queue_visual_polish_refresh(), add='+')
                    except Exception:
                        pass

        self._queue_visual_polish_refresh()

    def _display_path(self, path):
        """Return a readable path, using ~/ where possible."""
        try:
            return str(Path(path).expanduser()).replace(str(Path.home()), '~', 1)
        except Exception:
            return str(path)

    def _target_extension_for_current_settings(self):
        """Return the main print-target extension implied by Output Image Type."""
        imgtype = self.vars.get('printtarg_imgtype', tk.StringVar(value='')).get()
        if 'EPS' in imgtype:
            return '.eps'
        if 'TIFF' in imgtype:
            return '.tif'
        return '.ps'

    def _refresh_visual_polish(self):
        """Update the project summary and project-file status panels."""
        if not hasattr(self, 'project_summary_var') or not hasattr(self, 'project_files_var'):
            return

        def _do_refresh():
            try:
                printer = self.vars.get('printer_name', tk.StringVar(value='')).get().strip() or '—'
                paper = self.vars.get('paper_name', tk.StringVar(value='')).get().strip() or '—'
                ink = self.vars.get('ink_name', tk.StringVar(value='')).get().strip() or '—'
                basename = self.vars.get('basename', tk.StringVar(value='')).get().strip() or '—'
                patches = self.vars.get('patches', tk.StringVar(value='')).get().strip() or '—'
                paper_size = self.vars.get('paper_size', tk.StringVar(value='')).get().strip() or '—'
                target_arg = printtarg_paper_size_arg(paper_size)
                working_dir = self.get_working_dir()
                output_dir = self.vars.get('output_dir', tk.StringVar(value='')).get().strip() or '—'

                summary_lines = [
                    f"Project: {printer} / {paper} / {ink}",
                    f"Argyll basename: {basename}",
                    f"Target: {patches} patches; instrument {instrument_label(self.vars.get('printtarg_instrument', tk.StringVar(value='CM')).get())}; printtarg paper {paper_size}" + (f" ({target_arg})" if target_arg != paper_size else ""),
                    f"Expected layout: {patch_layout_note(patches, paper_size, self.vars.get('printtarg_instrument', tk.StringVar(value='CM')).get())}",
                    f"Working folder: {self._display_path(working_dir)}",
                    f"ICC output: {self._display_path(output_dir)}",
                ]
                self.project_summary_var.set("\n".join(summary_lines))

                if basename == '—':
                    self.project_files_var.set("No project files expected until a basename is available.")
                    return

                target_ext = self._target_extension_for_current_settings()
                candidates = [
                    ('.ti1', working_dir / f"{basename}.ti1"),
                    ('.ti2', working_dir / f"{basename}.ti2"),
                    ('.ti3', working_dir / f"{basename}.ti3"),
                    (target_ext, working_dir / f"{basename}{target_ext}"),
                    ('.icc', working_dir / f"{basename}.icc"),
                    ('.json', working_dir / f"{basename}.json"),
                    ('.log', working_dir / f"{basename}.log"),
                ]
                file_lines = []
                for label, path in candidates:
                    if path.exists():
                        try:
                            size = path.stat().st_size
                            state = f"present, {size:,} bytes"
                        except Exception:
                            state = "present"
                    else:
                        state = "not yet present"
                    file_lines.append(f"{label:<6} {state}")
                self.project_files_var.set("\n".join(file_lines))
            except Exception as e:
                self.project_summary_var.set(f"Project overview unavailable: {e}")
                self.project_files_var.set("File status unavailable.")

        self._ui_call(_do_refresh)

    def open_in_terminal(self, title, shell_script, cwd=None, hold_open=False):
        """Open a shell command/script in a real terminal window.

        This is shared by chartread and the man-page helpers so terminal
        selection is handled consistently.  Linux/*nix desktops are the primary
        target; macOS is supported through Terminal.app/osascript when present.
        """
        abs_cwd = os.path.abspath(cwd) if cwd else os.path.expanduser("~")
        run_script = f"cd {shlex.quote(abs_cwd)} && {shell_script}"
        if hold_open:
            run_script = f"{run_script}; echo ''; echo 'Press ENTER to close...'; read"

        self.log(f"Opening terminal: {title}")
        self.log(f"Terminal working directory: {abs_cwd}")

        # macOS: Terminal.app is controlled through AppleScript.  This path is
        # deliberately first on Darwin because macOS usually has no xterm-style
        # terminal command in PATH.
        if sys.platform == 'darwin' and shutil.which('osascript'):
            try:
                # Escape for an AppleScript string literal.
                applescript_string = run_script.replace('\\', '\\\\').replace('"', '\\"')
                mac_cmd = [
                    'osascript',
                    '-e', 'tell application "Terminal"',
                    '-e', 'activate',
                    '-e', f'do script "{applescript_string}"',
                    '-e', 'end tell',
                ]
                subprocess.Popen(
                    mac_cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True,
                    close_fds=True,
                )
                self.log("Launched in terminal: macOS Terminal.app")
                return True
            except Exception as e:
                self.log(f"WARNING: Could not launch macOS Terminal.app: {e}")
                # Fall through to the POSIX terminal list for users with
                # XQuartz/xterm or another terminal installed.

        # Common Linux/*nix terminal emulators.  Keep this conservative and
        # dependency-free; terminal availability is tested at runtime.
        terminal_commands = [
            ['gnome-terminal', f'--title={title}', '--', 'bash', '-lc', run_script],
            ['mate-terminal', '--title', title, '-e', f"bash -lc {shlex.quote(run_script)}"],
            ['xfce4-terminal', '--title', title, '-e', f"bash -lc {shlex.quote(run_script)}"],
            ['konsole', '--new-tab', '--workdir', abs_cwd, '-p', f'tabtitle={title}', '-e', 'bash', '-lc', run_script],
            ['xterm', '-T', title, '-e', 'bash', '-lc', run_script],
            ['terminator', '-T', title, '-e', f"bash -lc {shlex.quote(run_script)}"],
            ['x-terminal-emulator', '-e', 'bash', '-lc', run_script],
        ]

        for term_cmd in terminal_commands:
            if shutil.which(term_cmd[0]) is None:
                continue
            try:
                subprocess.Popen(
                    term_cmd,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True,
                    close_fds=True,
                )
                self.log(f"Launched in terminal: {term_cmd[0]}")
                return True
            except Exception as e:
                self.log(f"WARNING: Could not launch {term_cmd[0]}: {e}")

        return False

    def _man_page_available(self, command):
        """Return True only when the local man database contains this page."""
        if shutil.which('man') is None:
            return False
        try:
            result = subprocess.run(
                ['man', '-w', command],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=3,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            return False
        return result.returncode == 0 and bool(result.stdout.strip())

    def _open_local_man_page(self, command):
        """Open an available local man page in YAAW's detached terminal."""
        title = f'YAAW help: man {command}'
        shell_script = f"""
            printf '\\033]0;{title}\\007'
            {{
                printf 'YAAW / ArgyllCMS command help\\n'
                printf 'Command: man {command}\\n'
                printf 'Tool:    {command}\\n'
                printf '\\n'
                printf 'Close this terminal window when finished, or leave it open while editing YAAW settings.\\n'
                printf '======================================================================\\n\\n'
                man {shlex.quote(command)}
            }} | less -R
        """
        return self.open_in_terminal(
            title, shell_script, cwd=os.path.expanduser('~'), hold_open=False
        )

    def _local_argyll_html(self, command):
        """Return the locally discovered HTML documentation page, if present
        and readable. Files that exist but can't be read (e.g. an
        upstream tarball unpacked as root under /opt with restrictive
        permissions) are skipped rather than handed to the viewer, and
        the first such path is recorded in self._last_doc_permission_issue
        so callers can explain the problem instead of just failing.
        """
        filename = f'{command}.html'
        self._last_doc_permission_issue = None

        def _check(candidate):
            if not candidate.is_file():
                return None
            if not os.access(candidate, os.R_OK):
                if self._last_doc_permission_issue is None:
                    self._last_doc_permission_issue = candidate.resolve()
                return None
            return candidate.resolve()

        # Preferred source: the doc directory paired with the startup-discovered
        # upstream installation.
        if self.argyll_doc_dir is not None:
            found = _check(Path(self.argyll_doc_dir) / filename)
            if found is not None:
                return found

        # Repository packages may keep HTML independently of the executable.
        standard_dirs = (
            Path('/usr/share/doc/argyll'),
            Path('/usr/share/doc/argyll/html'),
            Path('/usr/share/doc/argyllcms'),
            Path('/usr/share/doc/argyllcms/html'),
            Path('/usr/share/argyll/doc'),
            Path('/usr/share/argyllcms/doc'),
            Path('/usr/local/share/doc/argyll'),
            Path('/usr/local/share/doc/argyllcms'),
        )
        for directory in standard_dirs:
            found = _check(directory / filename)
            if found is not None:
                return found
        return None

    def open_man_page(self, command):
        """Open local Argyll help, asking before using online documentation."""
        allowed = {'targen', 'printtarg', 'chartread', 'colprof'}
        if command not in allowed:
            self.show_error('Unknown command', f'No documentation helper is defined for: {command}')
            return

        # Native repository manpages remain the first preference.
        if self._man_page_available(command):
            if self._open_local_man_page(command):
                self.log(f'Opened man page: man {command}')
                return
            self.show_error(
                'Could not open man page',
                f'A local man page exists for {command}, but YAAW could not find a supported terminal emulator.'
            )
            return

        # Upstream releases provide linked HTML documentation instead.
        html_page = self._local_argyll_html(command)
        if html_page is not None:
            try:
                self._show_html_doc_window(f'ArgyllCMS documentation: {command}', html_page)
            except Exception as exc:
                self.show_error('Could not display documentation', f'Could not display:\n\n{html_page}\n\n{exc}')
                return
            self.log(f'Displayed local Argyll documentation: {html_page}')
            return

        # Never contact/open the online documentation without confirmation.
        permission_issue = getattr(self, '_last_doc_permission_issue', None)
        if permission_issue is not None:
            doc_root = permission_issue.parent
            prompt = (
                f'Local HTML documentation for {command} was found at:\n\n{permission_issue}\n\n'
                "but your user account doesn't have permission to read it. This is common when "
                'ArgyllCMS was installed as root under /opt without making the doc/ folder '
                'world-readable.\n\n'
                f'You can fix this from a terminal with:\n'
                f'  sudo chmod -R a+rX {doc_root}\n\n'
                'Display the official ArgyllCMS online documentation instead for now?'
            )
        else:
            prompt = (
                f'No installed man page or local HTML documentation was found for {command}.\n\n'
                'Display the official ArgyllCMS online documentation?'
            )
        if not self.ask_yes_no('Local Documentation Not Available', prompt):
            return

        url = f'https://www.argyllcms.com/doc/{command}.html'
        try:
            self._show_html_doc_window(f'ArgyllCMS online documentation: {command}', url)
        except Exception as exc:
            self.show_error('Could not display online documentation', f'Could not display:\n\n{url}\n\n{exc}')
            return
        self.log(f'Displayed official online Argyll documentation: {url}')

    def _resolve_local_doc_link(self, base_dir, href):
        """Resolve a link clicked inside local Argyll documentation to
        another local HTML file, if that's what it points to. Returns
        None for anchors, mailto links, or anything not resolving to a
        local .html/.htm file, so the caller can treat it as external.
        """
        if not href or href.startswith('#') or href.startswith('mailto:'):
            return None
        if href.startswith('http://') or href.startswith('https://'):
            return None
        clean = href.split('#', 1)[0].split('?', 1)[0]
        if not clean:
            return None
        try:
            candidate = (Path(base_dir) / clean).resolve()
        except Exception:
            return None
        if candidate.is_file() and candidate.suffix.lower() in ('.html', '.htm'):
            return candidate
        return None

    def _open_link_externally(self, url):
        """Open a link from the documentation viewer in the system browser."""
        try:
            opened = webbrowser.open_new(url)
        except Exception as exc:
            self.show_error('Could not open link', f'Could not open:\n\n{url}\n\n{exc}')
            return
        if opened is False:
            self.show_error('Could not open link', f'The web browser could not open:\n\n{url}')

    def _render_html_to_widget(self, text_widget, source, on_link):
        """Render an HTML document into a Tk Text widget using only the
        Python standard library and native tkinter (see
        _ArgyllHtmlParser). `source` is either a local Path or a URL
        string. Returns a dict mapping in-page anchor names (from
        id="..." or <a name="...">) to Tk text indices, so callers can
        support "#fragment" links.
        """
        try:
            if isinstance(source, Path):
                raw = source.read_text(encoding='utf-8', errors='replace')
            else:
                import urllib.request
                req = urllib.request.Request(source, headers={'User-Agent': 'YAAW/3.40'})
                with urllib.request.urlopen(req, timeout=8) as resp:
                    data = resp.read()
                    charset = resp.headers.get_content_charset() or 'utf-8'
                raw = data.decode(charset, errors='replace')
        except PermissionError as exc:
            text_widget.insert(
                'end',
                f"Permission denied reading:\n\n{source}\n\n"
                "Your user account doesn't have read access to this file. If ArgyllCMS was "
                "installed as root (e.g. under /opt), you can usually fix this with:\n\n"
                f"  sudo chmod -R a+rX {source.parent if isinstance(source, Path) else source}\n"
            )
            return {}
        except Exception as exc:
            text_widget.insert('end', f'Could not load {source}:\n\n{exc}')
            return {}

        family = 'TkDefaultFont'
        size = 10
        text_widget.tag_config('h1', font=(family, size + 6, 'bold'), spacing3=6)
        text_widget.tag_config('h2', font=(family, size + 4, 'bold'), spacing3=5)
        text_widget.tag_config('h3', font=(family, size + 2, 'bold'), spacing3=4)
        text_widget.tag_config('h4', font=(family, size + 1, 'bold'), spacing3=3)
        text_widget.tag_config('b', font=(family, size, 'bold'))
        text_widget.tag_config('i', font=(family, size, 'italic'))
        text_widget.tag_config('code', font=('TkFixedFont', size))
        text_widget.tag_config('pre', font=('TkFixedFont', size))
        text_widget.tag_config('link', foreground='#1a5fb4', underline=True)

        parser = _ArgyllHtmlParser(text_widget, on_link)
        try:
            parser.feed(raw)
            parser.close()
        except Exception as exc:
            text_widget.insert('end', f'\n\n[Documentation rendering stopped early: {exc}]')
        return parser.anchors

    def _show_html_doc_window(self, title, source):
        """Display ArgyllCMS HTML documentation inside a Tk window instead
        of handing off to an external browser, using only native tkinter
        widgets (see _render_html_to_widget / _ArgyllHtmlParser) - no
        external HTML/browser package is required or used.

        `source` is either a local Path (a page discovered on disk, which
        can be navigated in place by following links to other local pages)
        or a URL string (a single confirmed online page, shown read-only;
        links on it open in the system browser rather than being fetched
        automatically).
        """
        is_local = isinstance(source, Path)

        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry('920x700')
        window.transient(self.root)

        outer = ttk.Frame(window, padding=8)
        outer.pack(fill='both', expand=True)

        toolbar = ttk.Frame(outer)
        toolbar.pack(fill='x', pady=(0, 6))
        location_var = tk.StringVar(value=str(source))
        ttk.Label(toolbar, textvariable=location_var, anchor='w').pack(
            side='left', fill='x', expand=True
        )
        ttk.Button(toolbar, text='Close', command=window.destroy, width=10).pack(side='right')

        text_frame = ttk.Frame(outer)
        text_frame.pack(fill='both', expand=True)
        text_widget = tk.Text(
            text_frame, wrap='word', font=('TkDefaultFont', 10),
            padx=10, pady=8, cursor='arrow'
        )
        vsb = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        text_widget.pack(side='left', fill='both', expand=True)

        # Each history entry is {'loc': Path-or-URL, 'anchor': name-or-None}.
        # In-page anchor jumps push an entry with the same loc but a new
        # anchor, so Back can undo a same-page jump exactly like a
        # cross-page navigation - not just full document loads.
        history = [{'loc': source, 'anchor': None}]
        current_anchors = {}
        back_btn = None
        displayed_loc = [None]  # boxed so nested functions can update it

        def _sync_back_button():
            if back_btn is not None:
                if len(history) > 1:
                    back_btn.state(['!disabled'])
                else:
                    back_btn.state(['disabled'])

        def _load_page(loc):
            location_var.set(str(loc))
            text_widget.configure(state='normal')
            text_widget.delete('1.0', 'end')
            current_anchors.clear()
            current_anchors.update(self._render_html_to_widget(text_widget, loc, on_link))
            text_widget.configure(state='disabled')
            displayed_loc[0] = loc

        def _display(entry):
            loc = entry['loc']
            anchor = entry['anchor']
            if displayed_loc[0] != loc:
                _load_page(loc)
            if anchor:
                idx = current_anchors.get(anchor)
                if idx is not None:
                    text_widget.see(idx)
            else:
                text_widget.see('1.0')
            _sync_back_button()

        def _navigate(entry):
            history.append(entry)
            _display(entry)

        def on_link(href):
            if not href or href.startswith('mailto:'):
                return
            if href.startswith('http://') or href.startswith('https://'):
                self._open_link_externally(href)
                return
            file_part, has_fragment, fragment = href.partition('#')
            if not file_part:
                # Pure in-page anchor, e.g. a "Usage" contents list
                # jumping down to a heading further down this same page.
                if fragment:
                    _navigate({'loc': displayed_loc[0], 'anchor': fragment})
                return
            if is_local:
                resolved = self._resolve_local_doc_link(source.parent, file_part)
                if resolved is not None:
                    _navigate({'loc': resolved, 'anchor': fragment or None})
                    return
            # Not resolvable as a local page (or this is a single confirmed
            # online page) - nothing more we can safely do without fetching
            # further remote pages, which YAAW doesn't do automatically.

        def go_back():
            if len(history) > 1:
                history.pop()
                _display(history[-1])

        if is_local:
            back_btn = ttk.Button(toolbar, text='\u2190 Back', command=go_back, width=10)
            back_btn.pack(side='left', padx=(0, 8))
        _load_page(source)
        _sync_back_button()

        return window

    def browse_working_dir(self):
        """Browse for working directory"""
        current_dir = self.vars['working_dir'].get()
        initial_dir = current_dir if current_dir and os.path.exists(current_dir) else str(WORKING_ROOT)
        os.makedirs(initial_dir, exist_ok=True)
        directory = filedialog.askdirectory(
            initialdir=initial_dir,
            title="Select Working Directory"
        )
        if directory:
            self.vars['working_dir'].set(directory)

    def browse_output_dir(self):
        """Browse for output directory"""
        current_dir = self.vars['output_dir'].get()
        browse_root = str(ICC_OUTPUT_ROOT)
        os.makedirs(browse_root, exist_ok=True)
        initial_dir = current_dir if current_dir and os.path.exists(current_dir) else browse_root

        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=initial_dir
        )

        if directory:
            self.vars['output_dir'].set(directory)

    def browse_rendering_profile(self):
        """Browse for rendering ICC profile"""
        current_file = self.vars['rendering_profile'].get()
        browse_root = str(PROFILE_BROWSE_ROOT)
        if current_file and os.path.isabs(current_file):
            candidate = os.path.dirname(current_file)
            initial_dir = candidate if os.path.exists(candidate) else browse_root
        else:
            initial_dir = browse_root

        filename = filedialog.askopenfilename(
            title="Select Rendering ICC Profile",
            initialdir=initial_dir,
            filetypes=[("ICC Profiles", "*.icc"), ("All files", "*.*")]
        )

        if filename:
            self.vars['rendering_profile'].set(filename)
    
    def create_exec_tab(self, parent):
        """Create execution tab with workflow buttons and log"""
        # Status section
        status_frame = ttk.LabelFrame(parent, text="Status", padding="10")
        status_frame.pack(fill='x', padx=5, pady=5)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                font=('TkDefaultFont', 12, 'bold'))
        status_label.pack()
        
        # Workflow buttons
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Step 1: Create Target", 
                   command=self.run_step1, width=20, style="YAAWPrimary.TButton").pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Step 2: Print Target", 
                   command=self.run_step2, width=20, style="YAAWPrimary.TButton").pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Step 3: Read Target", 
                   command=self.run_step3, width=20, style="YAAWPrimary.TButton").pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Step 4: Build Profile", 
                   command=self.run_step4, width=20, style="YAAWPrimary.TButton").pack(side='left', padx=5)
        
        # Log output section
        log_frame = ttk.LabelFrame(parent, text="Log Output", padding="10")
        log_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=20,
            wrap=tk.WORD,
            font=('TkFixedFont', 10),
            background=self._yaaw_output_bg,
            foreground=self._yaaw_text,
            insertbackground=self._yaaw_text,
            selectbackground=self._yaaw_accent,
            selectforeground='white',
        )
        self.log_text.pack(fill='both', expand=True)
        # Keep live output independently of the widget so the same pane can
        # temporarily display the persistent logfile without losing new output.
        self._live_output_text = ""
        self._showing_project_log = False
        
        # Control buttons
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill='x', padx=5, pady=5)
        
        self.clear_window_button = ttk.Button(
            control_frame,
            text="Clear Window",
            command=self.clear_log,
            style="YAAWAction.TButton"
        )
        self.clear_window_button.pack(side='left', padx=5)

        self.current_settings_button = ttk.Button(
            control_frame,
            text="Current Settings",
            command=self.show_current_settings,
            style="YAAWAction.TButton"
        )
        self.current_settings_button.pack(side='left', padx=5)

        # Inspection tools live under Details rather than cluttering the normal
        # workflow view.  The Details/Live Output toggle itself remains packed in
        # one fixed position; only its label changes.
        self.details_gamut_button = ttk.Button(
            control_frame,
            text="Show Gamut",
            command=self.show_gamut_viewer,
            style="YAAWAction.TButton"
        )
        self.profcheck_3d_button = ttk.Button(
            control_frame,
            text="3D Error Map",
            command=self.open_profcheck_3d_model,
            style="YAAWAction.TButton"
        )
        self.view_log_button = ttk.Button(
            control_frame,
            text="Details",
            command=self.toggle_project_log_view,
            style="YAAWAction.TButton"
        )
        self.view_log_button.pack(side='left', padx=5)
        self.view_log_button.state(['disabled'])
        ttk.Button(control_frame, text="Abort", command=self.abort_session, style="YAAWAction.TButton").pack(side='right', padx=5)
    
    def create_about_tab(self, parent):
        """Create about tab with information"""
        about_text = """
YAAW Printer Profiling Tool for ColorMunki or Similar
====================================================

This tool provides a graphical interface for creating ICC printer profiles
using ArgyllCMS and the ColorMunki spectrophotometer.

Workflow:
1. Configure printer, paper, and ink details
2. Generate test target (targen)
3. Print target file (printtarg) - automatically opens for printing
4. Measure printed target (chartread) - follow on-screen instructions
5. Build ICC profile (colprof)

Features:
- Automatic field population based on printer/paper/ink
- Session persistence and crash recovery
- Progress tracking with detailed logging
- Instrument-specific patch-layout tables, with editable Instrument, Patches, and Paper Size fields
- Configurable output directory (default: ~/.local/share/color/icc)
- Support for ICC profile preconditioning
- Automatic opening of print targets in image viewer
- Multi-page target support for large patch counts
- ColorMunki layouts are author-tested; i1/i1Pro3+ layouts are printtarg-generated and need physical-device confirmation
- Optional additional Argyll arguments for targen, printtarg, chartread, and colprof
- One-click documentation buttons for targen, printtarg, chartread, and colprof, displayed in a built-in viewer (no external browser required)

Requirements:
- ArgyllCMS tools (targen, printtarg, chartread, colprof, profcheck)
- Supported ArgyllCMS strip-reading spectrophotometer, typically ColorMunki, i1Pro, or i1Pro3+
- Python 3.x with tkinter

Installation:
Ubuntu/Debian: sudo apt install argyll
Fedora/RHEL:   sudo dnf install argyll
macOS:         brew install argyll-cms

For more information:
- ArgyllCMS: https://www.argyllcms.com/
- ColorMunki: https://calibrite.com/

Version: 3.40.23
Copyright: Richard Lindner and contributors
Coding assistance: Anthropic Claude; OpenAI ChatGPT
License: MIT
        """
        
        text_widget = scrolledtext.ScrolledText(
            parent,
            wrap=tk.WORD,
            height=25,
            background=self._yaaw_output_bg,
            foreground=self._yaaw_text,
            insertbackground=self._yaaw_text,
            selectbackground=self._yaaw_accent,
            selectforeground='white',
        )
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        text_widget.insert('1.0', about_text)
        text_widget.config(state='disabled')
    
    def create_field(self, parent, var_name, label, default, tooltip="", width=40):
        """Create a labeled entry field"""
        frame = ttk.Frame(parent)
        frame.pack(fill='x', pady=2)

        ttk.Label(frame, text=label, width=25).pack(side='left')

        self.vars[var_name] = tk.StringVar(value=default)
        entry = ttk.Entry(
            frame,
            textvariable=self.vars[var_name],
            width=width
        )
        entry.pack(side='left', padx=5)

        if tooltip:
            ttk.Label(
                frame,
                text=f"({tooltip})",
                foreground='#555555',
                font=('TkDefaultFont', 9)
            ).pack(side='left')
    
    def _current_auto_basename(self):
        """Return the operational Argyll basename, including instrument and patch count.

        The generated filenames include both the selected instrument and patch
        count so different CM/i1/3p runs for the same printer/paper/ink do not
        overwrite each other.

        Example: IP8700_AusjetGloss_GI63-Argyll_CM_460
        """
        printer = self.vars['printer_name'].get().strip()
        paper = self.vars['paper_name'].get().strip()
        ink = self.vars['ink_name'].get().strip()
        patches = self.vars.get('patches', tk.StringVar(value="")).get().strip()
        instrument = self.vars.get('printtarg_instrument', tk.StringVar(value="CM")).get().strip()

        if not (printer and paper and ink):
            return ""

        inst_token = safe_filename_token(normalise_instrument_code(instrument), 'CM')
        patch_token = safe_filename_token(patches, 'custom') if patches else 'custom'
        return f"{printer}_{paper}_{ink}-Argyll_{inst_token}_{patch_token}"

    def _current_auto_profile_id(self):
        """Return the auto-generated profile description.

        It intentionally matches the operational basename so the visible
        profile description and the generated files identify the patch count.
        """
        return self._current_auto_basename()

    def _looks_auto_profile_id(self, value):
        """Return True if a value looks like one of our generated profile IDs.

        This is deliberately permissive so older sessions such as
        IP8700_AusjetGloss_GI63-Argyll are upgraded to the newer
        IP8700_AusjetGloss_GI63-Argyll_CM_420 form.  It also copes with
        paper/ink names that themselves contain underscores.
        """
        value = (value or "").strip()
        if not value:
            return True

        last_auto = getattr(self, '_last_auto_profile_id', '')
        if last_auto and value == last_auto:
            return True

        # Old auto-generated form without patch count.
        if value.endswith('-Argyll'):
            return True

        # Older auto-generated form with patch count only, plus the newer
        # instrument+patch form: -Argyll_420 or -Argyll_CM_420.
        if '-Argyll_' in value:
            suffix = value.rsplit('-Argyll_', 1)[1]
            if suffix.isdigit():
                return True
            parts = suffix.split('_')
            if len(parts) >= 2 and parts[-1].isdigit():
                return True

        return False

    def autofill_fields(self):
        """Auto-populate dependent fields based on printer/paper/ink/patch count.

        KISS behaviour: the profile identity is derived directly from the
        Printer/Paper/Ink fields plus the current instrument and targen patch count.  This
        keeps the visible Profile Description, the Base Filename, and the
        colprof -D description in lock-step, e.g.

            IP8700_AusjetGloss_GI63-Argyll_CM_420

        If the Patches value changes, all three fields update immediately.
        """
        auto_value = self._current_auto_profile_id()
        auto_basename = self._current_auto_basename()

        if auto_value:
            self.vars['profile_desc'].set(auto_value)
            self.vars['basename'].set(auto_basename)
            self.vars['colprof_description'].set(auto_value)
            self._last_auto_profile_id = auto_value
            self._last_synced_colprof_desc = auto_value

        # Update working_dir to reflect output_dir/basename
        self._update_working_dir()

        # Refresh overview after all auto-filled fields have settled.
        self._queue_visual_polish_refresh()

        # Auto-save on change, then refresh the read-only overview from the
        # current committed values.
        self._ui_call(self.save_session)
        self._queue_visual_polish_refresh()

    def _sync_colprof_description(self):
        """Keep colprof_description in sync with profile_desc,
        unless the user has manually entered a different value."""
        desc     = self.vars['profile_desc'].get()
        col_desc = self.vars['colprof_description'].get()
        last     = getattr(self, '_last_synced_colprof_desc', None)
        # Sync if colprof field is empty, already matches profile_desc,
        # or still holds the last value we auto-filled (not manually changed)
        if not col_desc or col_desc == desc or col_desc == last:
            self.vars['colprof_description'].set(desc)
            self._last_synced_colprof_desc = desc

    def _update_working_dir(self):
        """Keep working_dir in sync with WORKING_ROOT/basename.
        This is independent of output_dir — changing output_dir has no effect here.
        The -Argyll suffix is stripped from basename for the directory name."""
        basename = self.vars.get('basename', tk.StringVar()).get().strip()
        working_base = str(WORKING_ROOT)
        if basename:
            dir_name = strip_argyll_suffix(basename)
            self.vars['working_dir'].set(os.path.join(working_base, dir_name))
        else:
            self.vars['working_dir'].set(working_base)
    

    def browse_precond_profile(self):
        """Browse for preconditioning ICC profile"""
        current_file = self.vars['precond_profile'].get()
        browse_root = str(WORKING_ROOT)
        os.makedirs(browse_root, exist_ok=True)
        if current_file and os.path.isabs(current_file):
            candidate = os.path.dirname(current_file)
            initial_dir = candidate if os.path.exists(candidate) else browse_root
        else:
            initial_dir = browse_root

        filename = filedialog.askopenfilename(
            title="Select Preconditioning ICC Profile",
            initialdir=initial_dir,
            filetypes=[("ICC Profiles", "*.icc"), ("All files", "*.*")]
        )

        if filename:
            self.vars['precond_profile'].set(filename)


    def _dialog_width(self):
        """Return a compact wrap width for YAAW's own popup dialogs."""
        # Keep this deliberately close to the Load Config popup style.  Do not
        # scale it from the main window: that was what made warning dialogs feel
        # like noticeboards instead of small prompts.
        return 520

    def _dialog_font(self):
        """Return a modest normal-weight font for popup body text."""
        try:
            import tkinter.font as tkfont
            font = tkfont.nametofont('TkDefaultFont').copy()
            size = font.cget('size')
            if isinstance(size, int):
                if size > 10:
                    font.configure(size=10)
                elif size < -13:
                    font.configure(size=-13)
            font.configure(weight='normal')
            return font
        except Exception:
            return ('TkDefaultFont', 10, 'normal')

    def _wrap_dialog_message(self, message, chars=64):
        """Pre-wrap long generated filenames while preserving blank lines."""
        import textwrap
        wrapped = []
        for line in str(message).splitlines() or ['']:
            if not line:
                wrapped.append('')
            else:
                wrapped.append(textwrap.fill(
                    line,
                    width=chars,
                    break_long_words=True,
                    break_on_hyphens=False
                ))
        return '\n'.join(wrapped)

    def _centre_dialog(self, dialog):
        """Centre a popup over the main YAAW window."""
        try:
            dialog.update_idletasks()
            w = dialog.winfo_reqwidth()
            h = dialog.winfo_reqheight()
            root_x = self.root.winfo_rootx()
            root_y = self.root.winfo_rooty()
            root_w = self.root.winfo_width()
            root_h = self.root.winfo_height()
            x = root_x + max(20, (root_w - w) // 2)
            y = root_y + max(20, (root_h - h) // 3)
            screen_w = dialog.winfo_screenwidth()
            screen_h = dialog.winfo_screenheight()
            x = min(max(20, x), max(20, screen_w - w - 40))
            y = min(max(20, y), max(20, screen_h - h - 60))
            dialog.geometry(f'+{x}+{y}')
        except Exception:
            pass

    def _dialog_message_widget(self, parent, message):
        """Create the plain message area used by YAAW dialogs."""
        # Use a classic tk.Label with an explicit modest font rather than a
        # themed ttk.Label.  This keeps the warning text visually aligned with
        # the simple Load Config popup across Linux themes and avoids the large
        # bold stock-messagebox look.
        try:
            bg = parent.winfo_toplevel().cget('background')
        except Exception:
            bg = self.root.cget('background')
        label = tk.Label(
            parent,
            text=self._wrap_dialog_message(message),
            justify='left',
            anchor='nw',
            wraplength=self._dialog_width(),
            font=self._dialog_font(),
            bg=bg,
            padx=0,
            pady=0,
        )
        label.pack(fill='both', expand=True)
        return label

    def _show_text_dialog(self, title, message, kind='info'):
        """Show a compact YAAW popup instead of Tk's narrow messagebox."""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.transient(self.root)
        dialog.resizable(False, False)

        outer = ttk.Frame(dialog, padding=10)
        outer.pack(fill='both', expand=True)
        self._dialog_message_widget(outer, message)

        buttons = ttk.Frame(outer)
        buttons.pack(fill='x', pady=(8, 0))
        ok = ttk.Button(buttons, text='OK', command=dialog.destroy, width=10)
        ok.pack(side='right')
        dialog.bind('<Return>', lambda e: dialog.destroy())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        dialog.protocol('WM_DELETE_WINDOW', dialog.destroy)

        self._centre_dialog(dialog)
        try:
            dialog.grab_set()
            ok.focus_set()
            self.root.wait_window(dialog)
        except Exception:
            pass

    def ask_yes_no(self, title, message, default='yes'):
        """Show a compact Yes/No dialog and return True for Yes."""
        result = {'value': None}
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.transient(self.root)
        dialog.resizable(False, False)

        outer = ttk.Frame(dialog, padding=10)
        outer.pack(fill='both', expand=True)
        self._dialog_message_widget(outer, message)

        def choose(value):
            result['value'] = value
            dialog.destroy()

        buttons = ttk.Frame(outer)
        buttons.pack(fill='x', pady=(8, 0))
        no_btn = ttk.Button(buttons, text='No', command=lambda: choose(False), width=10)
        yes_btn = ttk.Button(buttons, text='Yes', command=lambda: choose(True), width=10)
        no_btn.pack(side='right')
        yes_btn.pack(side='right', padx=(0, 6))

        dialog.bind('<Escape>', lambda e: choose(False))
        dialog.protocol('WM_DELETE_WINDOW', lambda: choose(False))
        dialog.bind('<Return>', lambda e: choose(default == 'yes'))

        self._centre_dialog(dialog)
        try:
            dialog.grab_set()
            (yes_btn if default == 'yes' else no_btn).focus_set()
            self.root.wait_window(dialog)
        except Exception:
            return False
        return bool(result['value'])

    def _ui_call(self, func, *args, **kwargs):
        """Run a UI function safely from either the Tk thread or a worker thread."""
        if threading.current_thread() is self.main_thread:
            return func(*args, **kwargs)
        self.root.after(0, lambda: func(*args, **kwargs))

    def _ui_call_wait(self, func, *args, **kwargs):
        """Run a UI-thread function and return its result to a worker thread."""
        if threading.current_thread() is self.main_thread:
            return func(*args, **kwargs)

        completed = threading.Event()
        result = {}

        def invoke():
            try:
                result['value'] = func(*args, **kwargs)
            except Exception as exc:
                result['error'] = exc
            finally:
                completed.set()

        self.root.after(0, invoke)
        completed.wait()
        if 'error' in result:
            raise result['error']
        return result.get('value')

    def set_status(self, message):
        """Set the status label safely from worker threads."""
        if hasattr(self, 'status_var'):
            self._ui_call(self.status_var.set, message)

    def show_error(self, title, message):
        """Show an error dialog safely from worker threads."""
        self._ui_call(self._show_text_dialog, title, message, 'error')

    def show_warning(self, title, message):
        """Show a warning dialog safely from worker threads."""
        self._ui_call(self._show_text_dialog, title, message, 'warning')

    def show_info(self, title, message):
        """Show an information dialog safely from worker threads."""
        self._ui_call(self._show_text_dialog, title, message, 'info')

    def log(self, message):
        """Add message to screen log and, once a workflow step has started,
        also append it to the persistent per-project run log.
        """
        def _append():
            if not hasattr(self, 'log_text'):
                return
            text = str(message)
            rendered = f"{text}\n"
            self._live_output_text = getattr(self, '_live_output_text', '') + rendered
            if not getattr(self, '_showing_project_log', False):
                self.log_text.insert(tk.END, rendered)
                self.log_text.see(tk.END)

            # Persistent log: only active after a workflow step calls
            # _activate_project_log().  This avoids creating project files
            # while the user is still typing in the configuration screen.
            log_file = getattr(self, 'run_log_file', None)
            if log_file and not getattr(self, '_run_log_failed', False):
                try:
                    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    with open(log_file, 'a', encoding='utf-8') as f:
                        for line in text.splitlines() or ['']:
                            f.write(f"[{ts}] {line}\n")
                except Exception:
                    # Do not interrupt profiling because the audit log failed.
                    self._run_log_failed = True

            self.root.update_idletasks()
        self._ui_call(_append)
    
    def get_project_log_path(self):
        """Return the persistent per-job run log path beside the Argyll files."""
        basename = self.vars.get('basename', tk.StringVar()).get().strip()
        if not basename:
            return None
        return self.get_working_dir() / f"{basename}.log"

    def _activate_project_log(self, basename, step_name):
        """Start appending screen-log messages to a persistent run log.

        The project log is intentionally activated only when a workflow step is
        run, not during field editing.  It records the actual command flow and
        diagnostics printed to the GUI log, including expanded Argyll commands.
        """
        try:
            path = self.get_working_dir() / f"{basename}.log"
            path.parent.mkdir(parents=True, exist_ok=True)
            self.run_log_file = path
            self._run_log_failed = False

            header = [
                "",
                "=" * 72,
                f"YAAW persistent run log opened: {datetime.now().isoformat(timespec='seconds')}",
                f"Step: {step_name}",
                f"Basename: {basename}",
                f"Working directory: {self.get_working_dir()}",
                f"Script version: 3.40.3-internal4",
                "=" * 72,
            ]
            with open(path, 'a', encoding='utf-8') as f:
                for line in header:
                    f.write(line + "\n")
            self.log(f"Persistent run log: {path}")
            self._refresh_visual_polish()
        except Exception as e:
            self.run_log_file = None
            self._run_log_failed = True
            self.log(f"WARNING: Could not open persistent run log: {e}")
    
    def clear_log(self):
        """Clear the live Execution output without altering the project logfile."""
        self._live_output_text = ""
        if not getattr(self, '_showing_project_log', False):
            self.log_text.delete('1.0', tk.END)

    def _replace_execution_display(self, content):
        """Replace the visible Execution text without changing either source."""
        self.log_text.delete('1.0', tk.END)
        self.log_text.insert('1.0', content)
        self.log_text.see(tk.END)

    def _current_working_profile_exists(self):
        """Return True when the current project has a completed working ICC.

        This deliberately checks the ICC beside the project's Argyll files, not
        an older installed copy under the output profile directory.
        """
        basename_var = self.vars.get('basename')
        basename = basename_var.get().strip() if basename_var is not None else ''
        if not basename:
            return False
        return (self.get_working_dir() / f"{basename}.icc").is_file()

    def _reset_execution_to_live_output(self):
        """Return the Execution pane to its normal live-output state.

        Loading a different project must never leave the previous project's
        logfile or Details controls visible.
        """
        if not hasattr(self, 'log_text'):
            return

        self._showing_project_log = False
        self._replace_execution_display(getattr(self, '_live_output_text', ''))

        if hasattr(self, 'view_log_button'):
            self.view_log_button.configure(text='Details')
        if hasattr(self, 'details_gamut_button'):
            self.details_gamut_button.pack_forget()
        if hasattr(self, 'profcheck_3d_button'):
            self.profcheck_3d_button.pack_forget()

        if hasattr(self, 'clear_window_button') and hasattr(self, 'view_log_button'):
            self.clear_window_button.pack_forget()
            self.clear_window_button.pack(
                side='left', padx=5, before=self.view_log_button
            )
        if hasattr(self, 'current_settings_button') and hasattr(self, 'view_log_button'):
            self.current_settings_button.pack_forget()
            self.current_settings_button.pack(
                side='left', padx=5, before=self.view_log_button
            )

        self.set_status('Live output')

    def _set_details_available(self, available):
        """Enable Details only after a successful current Step 4 result."""
        available = bool(available)
        self._details_available = available

        # Do not leave stale project details visible when a new workflow run
        # invalidates them.
        if not available and getattr(self, '_showing_project_log', False):
            self.toggle_project_log_view()

        if hasattr(self, 'view_log_button'):
            if available:
                self.view_log_button.state(['!disabled'])
            else:
                self.view_log_button.state(['disabled'])

    def toggle_project_log_view(self):
        """Toggle the main Execution pane between Details and live output."""
        if (not getattr(self, '_showing_project_log', False)
                and not getattr(self, '_details_available', False)):
            return

        if getattr(self, '_showing_project_log', False):
            self._showing_project_log = False
            self._replace_execution_display(getattr(self, '_live_output_text', ''))
            if hasattr(self, 'view_log_button'):
                self.view_log_button.configure(text='Details')
            if hasattr(self, 'details_gamut_button'):
                self.details_gamut_button.pack_forget()
            if hasattr(self, 'profcheck_3d_button'):
                self.profcheck_3d_button.pack_forget()

            # Restore the normal live-output controls before the fixed toggle.
            if hasattr(self, 'clear_window_button'):
                self.clear_window_button.pack(
                    side='left', padx=5, before=self.view_log_button
                )
            if hasattr(self, 'current_settings_button'):
                self.current_settings_button.pack(
                    side='left', padx=5, before=self.view_log_button
                )

            self.set_status('Live output')
            return

        path = getattr(self, 'run_log_file', None) or self.get_project_log_path()
        if not path or not Path(path).exists():
            self.show_warning(
                "Details",
                "No persistent project log exists yet. Run a workflow step first."
            )
            return

        try:
            content = Path(path).read_text(encoding='utf-8', errors='replace')
        except OSError as exc:
            self.show_error("Details", f"Could not read the project log:\n{path}\n\n{exc}")
            return

        self._showing_project_log = True
        self._replace_execution_display(content)

        if hasattr(self, 'view_log_button'):
            self.view_log_button.configure(text='Live Output')

        # Clear Window and Current Settings apply to live output rather than the
        # persistent logfile, so hide them in Details mode. Their two positions
        # are then occupied by Show Gamut and 3D Error Map, leaving the toggle
        # exactly where Details was.
        if hasattr(self, 'clear_window_button'):
            self.clear_window_button.pack_forget()
        if hasattr(self, 'current_settings_button'):
            self.current_settings_button.pack_forget()

        if hasattr(self, 'details_gamut_button'):
            self.details_gamut_button.pack(
                side='left', padx=5, before=self.view_log_button
            )

        # Older completed projects may predate X3DOM generation. Build only
        # the missing profcheck error map from their existing TI3 and ICC.
        self._ensure_profcheck_3d_model()
        model_path = self.get_profcheck_3d_model_path()
        if model_path and model_path.exists() and hasattr(self, 'profcheck_3d_button'):
            self.profcheck_3d_button.pack(
                side='left', padx=5, before=self.view_log_button
            )
        elif hasattr(self, 'profcheck_3d_button'):
            self.profcheck_3d_button.pack_forget()

        self.set_status(f"Viewing project details: {Path(path).name}")

    def get_profcheck_3d_model_path(self):
        """Return the expected profcheck X3DOM HTML path for this project."""
        basename_var = self.vars.get('basename')
        basename = basename_var.get().strip() if basename_var is not None else ''
        if not basename:
            return None
        return self.get_working_dir() / f"{basename}.x3d.html"

    def _ensure_profcheck_3d_model(self):
        """Generate a missing profcheck X3DOM for an older completed project.

        This is deliberately limited to the existing measured TI3 and working
        ICC. It does not rerun colprof or otherwise rebuild the profile.
        """
        model_path = self.get_profcheck_3d_model_path()
        if model_path and model_path.is_file():
            return True

        basename_var = self.vars.get('basename')
        basename = basename_var.get().strip() if basename_var is not None else ''
        if not basename:
            return False

        working_dir = self.get_working_dir()
        ti3_path = working_dir / f"{basename}.ti3"
        icc_path = working_dir / f"{basename}.icc"
        if not ti3_path.is_file() or not icc_path.is_file():
            return False

        self.set_status("Generating 3D Error Map...")
        try:
            result = subprocess.run(
                [
                    'profcheck', '-v2', '-s', '-w', '-x', '-m',
                    ti3_path.name, icc_path.name
                ],
                cwd=str(working_dir),
                capture_output=True,
                text=True,
                timeout=120
            )
        except FileNotFoundError:
            self.log("WARNING: profcheck not found; could not generate the 3D Error Map.")
            return False
        except subprocess.TimeoutExpired:
            self.log("WARNING: profcheck timed out while generating the 3D Error Map.")
            return False
        except OSError as exc:
            self.log(f"WARNING: Could not generate the 3D Error Map: {exc}")
            return False

        if result.returncode != 0:
            detail = (result.stderr or result.stdout or '').strip()
            if detail:
                detail = detail[:600]
                self.log(
                    f"WARNING: profcheck could not generate the 3D Error Map "
                    f"(code {result.returncode}): {detail}"
                )
            else:
                self.log(
                    f"WARNING: profcheck could not generate the 3D Error Map "
                    f"(code {result.returncode})."
                )
            return False

        if model_path and model_path.is_file():
            self.log(
                f"Generated missing profcheck 3D Error Map for loaded project: "
                f"{model_path.name}"
            )
            return True

        self.log(
            "WARNING: profcheck completed but did not create the expected "
            f"3D Error Map: {model_path}"
        )
        return False

    def get_gamut_3d_model_path(self):
        """Return the independent iccgamut X3DOM HTML path for this project."""
        basename_var = self.vars.get('basename')
        basename = basename_var.get().strip() if basename_var is not None else ''
        if not basename:
            return None
        return self.get_working_dir() / f"{basename}-gamut.x3d.html"

    def open_gamut_3d_model(self):
        """Open iccgamut's generated interactive 3D gamut model in a browser."""
        path = self.get_gamut_3d_model_path()
        if not path or not path.exists():
            self.show_warning(
                "3D Gamut",
                "No iccgamut X3DOM model exists for the current profile.\n\n"
                "Open View Gamut again to generate it."
            )
            return
        try:
            opened = webbrowser.open_new(path.resolve().as_uri())
        except Exception as exc:
            self.show_error(
                "3D Gamut",
                f"Could not open the 3D gamut model:\n{path}\n\n{exc}"
            )
            return
        if not opened:
            self.show_error(
                "3D Gamut",
                f"The system browser could not open:\n{path}"
            )
            return
        self.set_status(f"Opened 3D gamut model: {path.name}")

    def open_profcheck_3d_model(self):
        """Open profcheck's generated interactive 3D error model in a browser."""
        path = self.get_profcheck_3d_model_path()
        if not path or not path.exists():
            self.show_warning(
                "X3DOM",
                "No profcheck X3DOM exists for the current project.\n\n"
                "Build the profile with Step 4 first."
            )
            return
        try:
            opened = webbrowser.open_new(path.resolve().as_uri())
        except Exception as exc:
            self.show_error(
                "X3DOM",
                f"Could not open the X3DOM:\n{path}\n\n{exc}"
            )
            return
        if not opened:
            self.show_error(
                "X3DOM",
                f"The system browser could not open:\n{path}"
            )
            return
        self.set_status(f"Opened 3D profcheck model: {path.name}")

    def show_current_settings(self):
        """Log the current key settings for easier audit/debugging before running Argyll."""
        basename = self.vars.get('basename', tk.StringVar()).get().strip()
        working_dir = self.get_working_dir()
        self.log("=== CURRENT PROFILE SETTINGS ===")
        self.log(f"Basename: {basename}")
        self.log(f"Working directory: {working_dir}")
        self.log(f"Output directory: {self.vars['output_dir'].get()}")
        patches = self.vars['patches'].get()
        paper_size = self.vars['paper_size'].get()
        printtarg_paper_size = printtarg_paper_size_arg(paper_size)
        paper_display = paper_size + (f" ({printtarg_paper_size})" if printtarg_paper_size != paper_size else "")
        self.log(f"Target: {patches} patches, instrument {self.vars['printtarg_instrument'].get()}, ink limit {self.vars['ink_limit'].get()}%, printtarg paper {paper_display}")
        self.log(f"Expected layout: {patch_layout_note(patches, paper_size, self.vars.get('printtarg_instrument', tk.StringVar(value='CM')).get())}")
        self.log(
            "targen neutral/grey: "
            f"grey={self.vars['targen_grey_steps'].get()}, "
            f"neutral={self.vars['targen_neutral_steps'].get()}, "
            f"N={self.vars['targen_neutral_emphasis'].get()}, "
            f"V={self.vars['targen_dark_emphasis'].get()}, "
            f"white={self.vars['targen_white_patches'].get()}, "
            f"black={self.vars['targen_black_patches'].get()}, "
            f"extra={self.vars.get('targen_extra_args', tk.StringVar()).get()}"
        )
        self.log(f"printtarg: instrument={self.vars['printtarg_instrument'].get()}, paper={self.vars['paper_size'].get()}, image={self.vars['printtarg_imgtype'].get()}, hex={self.vars['printtarg_hexagon'].get()}, extra={self.vars.get('printtarg_extra_args', tk.StringVar()).get()}")
        self.log(f"chartread: threshold={self.vars['chartread_threshold'].get()}, CIE={self.vars['chartread_cie'].get()}, high-res={self.vars['chartread_highres'].get()}, resume={self.vars['chartread_resume'].get()}, suppress warnings={self.vars['chartread_supwrn'].get()}, patch-by-patch={self.vars['chartread_patch_by_patch'].get()}, extra={self.vars.get('chartread_extra_args', tk.StringVar()).get()}")
        self.log(f"colprof: intent={self.vars['colprof_intent'].get()}, quality={self.vars['colprof_quality'].get()}, -r={self.vars['colprof_avgdev'].get()}, extra={self.vars.get('colprof_extra_args', tk.StringVar()).get()}")
        precond_display = (self.vars['precond_profile'].get() or '').strip()
        if not precond_display:
            self.log("Preconditioning profile: blank (targen -c omitted; Argyll default model used)")
        elif precond_display.lower() == 'none':
            self.log("Preconditioning profile: none (literal targen -c none; default model disabled)")
        else:
            self.log(f"Preconditioning profile: {precond_display}")
        if self.vars['rendering_profile'].get():
            self.log(f"Rendering/source profile: {self.vars['rendering_profile'].get()}")
        self.log("=== END SETTINGS ===")

    def _current_config_payload(self):
        """Return the current GUI configuration as a JSON-serialisable dict."""
        return {
            'vars': {k: v.get() for k, v in self.vars.items()},
            'timestamp': datetime.now().isoformat(),
            'yaaw_config_version': '3.39.10'
        }

    def get_project_config_path(self):
        """Return the automatic per-job config path in the working directory.

        The working directory deliberately omits the -Argyll_<patchcount> suffix,
        but the persistent project JSON should match the generated Argyll basename
        so multiple patch-count runs can coexist without ambiguous config names.
        Example:
            working dir: Printer_Paper_Ink/
            JSON:        Printer_Paper_Ink-Argyll_420.json
        """
        basename = self.vars.get('basename', tk.StringVar()).get().strip()
        if not basename:
            return None
        working_dir = self.get_working_dir()
        return working_dir / f"{basename}.json"

    def save_project_config(self, log_message=False):
        """Silently save the current job configuration beside the Argyll files.

        This is separate from the transient crash-recovery session file in ~/tmp.
        The project JSON is deliberately kept after a successful profile build.
        """
        path = self.get_project_config_path()
        if path is None:
            return None
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as f:
                json.dump(self._current_config_payload(), f, indent=2)
            if log_message:
                self.log(f"Saved project config: {path}")
            self._refresh_visual_polish()
            return path
        except Exception as e:
            if log_message:
                self.log(f"WARNING: Could not save project config: {e}")
            return None

    def save_config(self):
        """Save current configuration to file.

        The default save directory is the unsuffixed working directory, but the
        default JSON filename must preserve the operational Argyll basename,
        including -Argyll_<patchcount>.
        """
        # Make sure the visible auto-generated fields are in sync before using
        # them for the save-dialog defaults.  This avoids stale values if the
        # user has just changed printer/paper/ink/patches and immediately clicks
        # Save Config.
        self.autofill_fields()
        config = self._current_config_payload()

        full_basename = self._current_auto_basename() or self.vars.get('basename', tk.StringVar()).get().strip()
        dir_name = strip_argyll_suffix(full_basename)
        initial_dir = WORKING_ROOT / dir_name if dir_name else WORKING_ROOT
        initial_dir.mkdir(parents=True, exist_ok=True)

        # The directory deliberately omits -Argyll_<patchcount>, but the saved
        # project JSON filename should match the operational Argyll basename so
        # separate 210/420/etc. configurations do not overwrite or look alike.
        initial_file = f"{full_basename}.json" if full_basename else "config.json"

        file = filedialog.asksaveasfilename(
            initialdir=str(initial_dir),
            initialfile=initial_file,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if file:
            with open(file, 'w') as f:
                json.dump(config, f, indent=2)
            self.show_info("Success", "Configuration saved successfully")
    
    def _select_project_json_from_yaaw_tree(self):
        """Show all project JSON files under WORKING_ROOT and return one path.

        The native file dialog starts in one directory and does not present a
        recursive project list.  YAAW stores configs beside per-project Argyll
        files, so a small selector is clearer: it lists every *.json found under
        the YAAW working tree and lets the user filter/select explicitly.
        """
        root_dir = WORKING_ROOT.expanduser()
        root_dir.mkdir(parents=True, exist_ok=True)
        json_files = sorted(root_dir.rglob("*.json"), key=lambda p: str(p).lower())

        if not json_files:
            self.show_warning(
                "No Config Files Found",
                f"No JSON config files were found under:\n\n{root_dir}"
            )
            return None

        selected = {'path': None}

        dialog = tk.Toplevel(self.root)
        dialog.title("Load YAAW Config")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.geometry("900x500")

        outer = ttk.Frame(dialog, padding="10")
        outer.pack(fill='both', expand=True)

        ttk.Label(
            outer,
            text=f"Select a YAAW project config from {root_dir}",
            anchor='w'
        ).pack(fill='x', pady=(0, 6))

        filter_var = tk.StringVar(value="")
        filter_frame = ttk.Frame(outer)
        filter_frame.pack(fill='x', pady=(0, 6))
        ttk.Label(filter_frame, text="Filter:").pack(side='left')
        filter_entry = ttk.Entry(filter_frame, textvariable=filter_var)
        filter_entry.pack(side='left', fill='x', expand=True, padx=(6, 0))

        list_frame = ttk.Frame(outer)
        list_frame.pack(fill='both', expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical')
        listbox = tk.Listbox(list_frame, activestyle='dotbox')
        listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        status_var = tk.StringVar(value="")
        ttk.Label(outer, textvariable=status_var, anchor='w', foreground='gray').pack(fill='x', pady=(6, 0))

        current_items = []

        def display_name(path):
            try:
                return str(path.relative_to(root_dir))
            except Exception:
                return str(path)

        def refresh_list(*args):
            needle = filter_var.get().strip().lower()
            matches = [p for p in json_files if needle in display_name(p).lower()]
            current_items[:] = matches
            listbox.delete(0, tk.END)
            for p in matches:
                listbox.insert(tk.END, display_name(p))
            status_var.set(f"{len(matches)} of {len(json_files)} config file(s) shown")
            if matches:
                listbox.selection_set(0)
                listbox.activate(0)

        def choose_current(event=None):
            sel = listbox.curselection()
            if not sel:
                return
            selected['path'] = current_items[sel[0]]
            dialog.destroy()

        def cancel(event=None):
            selected['path'] = None
            dialog.destroy()

        filter_var.trace_add('write', refresh_list)
        listbox.bind('<Double-Button-1>', choose_current)
        listbox.bind('<Return>', choose_current)
        dialog.bind('<Escape>', cancel)

        buttons = ttk.Frame(outer)
        buttons.pack(fill='x', pady=(10, 0))
        ttk.Button(buttons, text="Cancel", command=cancel).pack(side='right', padx=(5, 0))
        ttk.Button(buttons, text="Load Selected", command=choose_current).pack(side='right')

        refresh_list()
        filter_entry.focus_set()

        self.root.wait_window(dialog)
        return selected['path']

    def load_config(self):
        """Load configuration from a project JSON selected from WORKING_ROOT."""
        file = self._select_project_json_from_yaaw_tree()

        if file:
            try:
                # A newly selected project must start from a clean Execution view.
                # Do this before changing any project identity or Details state.
                self._reset_execution_to_live_output()

                with open(file, 'r') as f:
                    config = json.load(f)

                # Restore the saved project identity exactly.  While loading,
                # suppress variable traces that would otherwise regenerate the
                # basename using the current naming convention.  This is vital
                # for older projects whose real files are named, for example,
                # ...-Argyll_460 rather than ...-Argyll_CM_460.
                loaded_vars = config.get('vars', {})
                self._loading_config = True
                try:
                    for k, v in loaded_vars.items():
                        if k == 'paper_size' and v == '594x420':
                            v = 'A2R'
                        if k in self.vars:
                            self.vars[k].set(v)
                finally:
                    self._loading_config = False

                # Very old/minimal configs may not contain an operational
                # basename.  Only in that case derive one from the visible
                # identity fields; otherwise preserve the saved value verbatim.
                if not self.vars.get('basename', tk.StringVar()).get().strip():
                    self.autofill_fields()
                else:
                    self._last_auto_profile_id = self.vars.get('profile_desc', tk.StringVar()).get().strip()
                    self._last_synced_colprof_desc = self.vars.get('colprof_description', tk.StringVar()).get().strip()
                    try:
                        self.patches_combo.configure(values=self._patch_values_for_current_instrument())
                    except Exception:
                        pass

                # A loaded completed project is immediately inspectable.  An
                # installed ICC elsewhere is not enough: Details belongs to this
                # working project and its own profile/log outputs.
                self._set_details_available(self._current_working_profile_exists())

                # Successful loads are silent; the updated Configuration screen is enough.
                self.set_status("Ready")
                self.notebook.select(0)
                self._queue_visual_polish_refresh()
            except Exception as e:
                self.show_error("Error", f"Failed to load configuration: {e}")

    def abort_session(self):
        """Clear all saved session data and return to Configuration tab"""
        if not self.ask_yes_no("Abort Session",
                "This will clear the transient auto-recovery session and return to the Configuration screen.\n\nIt will not delete project JSON files saved beside Argyll outputs.\n\nContinue?"):
            return

        # Delete the session file
        try:
            if self.config_file.exists():
                self.config_file.unlink()
        except Exception:
            pass

        # Reset all variables to defaults
        defaults = {
            'printer_name': '',
            'paper_name': '',
            'ink_name': '',
            'profile_desc': '',
            'basename': '',
            'patches': '460',
            'paper_size': 'A3',
            'output_dir': str(ICC_OUTPUT_ROOT),
            'working_dir': str(WORKING_ROOT),
            'ink_limit': '300',
            'precond_profile': '',
            'targen_grey_steps': '16',
            'targen_neutral_steps': '8',
            'targen_neutral_emphasis': '0.5',
            'targen_dark_emphasis': '1.0',
            'targen_white_patches': '4',
            'targen_black_patches': '4',
            'targen_extra_args': '',
            'printtarg_instrument': 'CM',
            'printtarg_imgtype': 'PS (Postscript)',
            'printtarg_hexagon': True,
            'printtarg_extra_args': '',
            'chartread_threshold': '1',
            'chartread_cie': 'Lab (-l)',
            'chartread_highres': True,
            'chartread_resume': False,
            'chartread_supwrn': False,
            'chartread_patch_by_patch': False,
            'chartread_extra_args': '',
            'rendering_profile': '',
            'colprof_intent': 'r - Rel. Colorimetric',
            'colprof_quality': 'h - High',
            'colprof_avgdev': '0.5',
            'colprof_extra_args': '',
            'colprof_description': '',
            'colprof_manufacturer': '',
            'colprof_model': '',
            'colprof_copyright': '',
        }
        for k, v in defaults.items():
            if k in self.vars:
                self.vars[k].set(v)

        # Clear log
        self.clear_log()

        # Reset status
        self.set_status("Ready")

        # Switch back to Configuration tab (index 0)
        self.notebook.select(0)

    def try_load_session_data(self):
        """Try to load session data without applying it yet"""
        session_file = self.config_file
        if session_file.exists():
            try:
                with open(session_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return None
    
    def apply_loaded_session(self):
        """Apply loaded session data to widgets"""
        if not self.loaded_session:
            return
        
        # Load variables (includes precond_profile)
        for k, v in self.loaded_session.get('vars', {}).items():
            if k == 'paper_size' and v == '594x420':
                v = 'A2R'
            if k in self.vars:
                self.vars[k].set(v)

        # Recompute derived fields so older saved sessions gain the patch-count
        # suffix in Profile Description / Base Filename / colprof -D.
        self.autofill_fields()
        self._set_details_available(self._current_working_profile_exists())
    
    def save_session(self, last_step_completed=None):
        """Save transient crash-recovery session only.

        Do not write the persistent per-job project JSON from here: this method
        is called by GUI field traces while the user is still typing.  Writing
        the project JSON here created a new working directory for every partial
        basename such as Printer_P, Printer_Pa, etc.
        """
        # Preserve existing last_step_completed if not explicitly updating it
        existing_step = 0
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    existing = json.load(f)
                existing_step = existing.get('last_step_completed', 0)
            except Exception:
                pass

        config = {
            'vars': {k: v.get() for k, v in self.vars.items()},
            'last_step_completed': last_step_completed if last_step_completed is not None else existing_step,
            'timestamp': datetime.now().isoformat()
        }

        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception:
            pass  # Silent fail on session save
        self._refresh_visual_polish()
    
    def validate_config(self):
        """Validate configuration before running workflow steps"""
        required = ['printer_name', 'paper_name', 'ink_name', 'basename']
        missing = [k for k in required if not self.vars[k].get()]
        
        if missing:
            self.show_error("Missing Information", 
                f"Please fill in: {', '.join(missing)}")
            return False
        
        # Validate output directory
        output_dir = self.vars['output_dir'].get()
        if not output_dir:
            self.show_error("Missing Information", "Please specify an output directory")
            return False
        
        return True

    def _add_extra_args(self, cmd, var_name, tool_name, raw_value=None):
        """Append optional raw Argyll option arguments from a GUI field.

        The field is parsed with shlex.split(), so quoted paths/values are
        supported. Extra arguments are appended before the final basename.

        This field is for extra Argyll *options*, not positional filenames.
        A bare token such as "Test" would be appended before the basename and
        may be interpreted by Argyll as an output basename or input file, so the
        first token must look like an option and start with '-'.  Option values
        may still follow normally, e.g. ``-S /path/to/source.icc`` or
        ``-D "description text"``.
        """
        if raw_value is None:
            var = self.vars.get(var_name)
            raw = var.get().strip() if var is not None else ""
        else:
            raw = str(raw_value).strip()
        if not raw:
            return
        try:
            extra = shlex.split(raw)
        except ValueError as e:
            raise Exception(f"Invalid {tool_name} additional arguments: {e}")

        if not extra:
            return

        if not extra[0].startswith('-'):
            raise Exception(
                f"Invalid {tool_name} additional arguments: {raw!r}\n\n"
                "Additional argument fields are for optional Argyll switches only. "
                "The first token must begin with '-' (for example: -S /path/to/source.icc).\n\n"
                "Bare filenames or basenames are not allowed here because they can be "
                "mistaken for Argyll input/output files."
            )

        self.log(f"Additional {tool_name} args: {shlex.join(extra)}")
        cmd.extend(extra)
    

    # === CGATS validation helpers ===

    def _read_cgats_sections(self, path):
        """Return CGATS DATA sections as [(columns, rows), ...]."""
        sections = []
        cur_cols = []
        cur_rows = []
        in_fmt = False
        in_data = False

        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith("#"):
                    continue

                if s == "BEGIN_DATA_FORMAT":
                    in_fmt = True
                    cur_cols = []
                    continue
                if s == "END_DATA_FORMAT":
                    in_fmt = False
                    continue
                if s == "BEGIN_DATA":
                    in_data = True
                    cur_rows = []
                    continue
                if s == "END_DATA":
                    in_data = False
                    sections.append((list(cur_cols), list(cur_rows)))
                    continue

                if in_fmt:
                    cur_cols.extend(s.split())
                elif in_data:
                    cur_rows.append(s.split())

        return sections

    def _rgb_rows_from_cgats(self, path):
        """Return RGB rows from all CGATS DATA sections.

        Each returned item is a dict containing r/g/b, sample_id, sample_loc,
        optional LAB_L, and section index.  Argyll .ti1 files can contain more
        than one DATA section; .ti2/.ti3 normally contain the printable/measured
        target section.  Do not assume a literal RGB 100/100/100 paper-white row
        will be present in .ti2/.ti3; printtarg often carries near-white instead.
        """
        rows_out = []
        sections = self._read_cgats_sections(path)

        for sec_idx, (cols, rows) in enumerate(sections, start=1):
            try:
                ir = cols.index("RGB_R")
                ig = cols.index("RGB_G")
                ib = cols.index("RGB_B")
            except ValueError:
                continue

            isid = cols.index("SAMPLE_ID") if "SAMPLE_ID" in cols else None
            iloc = cols.index("SAMPLE_LOC") if "SAMPLE_LOC" in cols else None
            ilab = cols.index("LAB_L") if "LAB_L" in cols else None

            for row in rows:
                if len(row) <= max(ir, ig, ib):
                    continue
                try:
                    item = {
                        "r": float(row[ir]),
                        "g": float(row[ig]),
                        "b": float(row[ib]),
                        "sample_id": row[isid] if isid is not None and len(row) > isid else "?",
                        "sample_loc": row[iloc] if iloc is not None and len(row) > iloc else "?",
                        "section": sec_idx,
                    }
                    if ilab is not None and len(row) > ilab:
                        try:
                            item["LAB_L"] = float(row[ilab])
                        except Exception:
                            pass
                    rows_out.append(item)
                except Exception:
                    continue

        return rows_out

    def count_rgb_white_rows(self, path):
        """Count rows where RGB_R/RGB_G/RGB_B are exactly 100.0000.

        This is now diagnostic only.  It must not be used as a hard validity
        test for .ti2/.ti3, because printtarg may omit literal RGB 100/100/100
        while still providing a near-white reference patch.
        """
        try:
            rows = self._rgb_rows_from_cgats(path)
        except Exception as e:
            self.log(f"WARNING: Could not parse {path}: {e}")
            return 0

        return sum(
            1 for row in rows
            if abs(row["r"] - 100.0) < 0.0001
            and abs(row["g"] - 100.0) < 0.0001
            and abs(row["b"] - 100.0) < 0.0001
        )

    def _fmt_rgb_row(self, row):
        """Format an RGB diagnostic row for the log."""
        if row is None:
            return "none"
        extra = ""
        if "LAB_L" in row:
            extra = f", L*={row['LAB_L']:.3f}"
        return (
            f"RGB=({row['r']:.5g}, {row['g']:.5g}, {row['b']:.5g}), "
            f"sample={row.get('sample_id', '?')}, loc={row.get('sample_loc', '?')}, "
            f"section={row.get('section', '?')}{extra}"
        )

    def rgb_endpoint_diagnostic(self, path, stage_name, measured=False):
        """Log RGB endpoint diagnostics for .ti1/.ti2/.ti3 without hard-failing.

        Earlier versions treated absence of a literal RGB 100/100/100 row as
        fatal.  Manual Argyll tests showed that printtarg can produce valid-looking
        .ti2 files whose nearest neutral white is about 93.333/93.333/93.333, not
        literal 100/100/100.  Therefore this routine reports exact-white count and
        nearest endpoints, warning only when the lightest patch is suspiciously dark.
        """
        try:
            rows = self._rgb_rows_from_cgats(path)
        except Exception as e:
            self.log(f"WARNING: {stage_name}: could not parse {Path(path).name}: {e}")
            return {"rows": 0, "exact_white": 0, "nearest_white": None, "nearest_black": None}

        exact_white = sum(
            1 for row in rows
            if abs(row["r"] - 100.0) < 0.0001
            and abs(row["g"] - 100.0) < 0.0001
            and abs(row["b"] - 100.0) < 0.0001
        )
        exact_black = sum(
            1 for row in rows
            if abs(row["r"]) < 0.0001
            and abs(row["g"]) < 0.0001
            and abs(row["b"]) < 0.0001
        )

        nearest_white = None
        nearest_black = None
        max_sum = None
        min_sum = None
        if rows:
            nearest_white = min(rows, key=lambda x: (100-x["r"])**2 + (100-x["g"])**2 + (100-x["b"])**2)
            nearest_black = min(rows, key=lambda x: x["r"]**2 + x["g"]**2 + x["b"]**2)
            max_sum = max(rows, key=lambda x: x["r"] + x["g"] + x["b"])
            min_sum = min(rows, key=lambda x: x["r"] + x["g"] + x["b"])

        self.log(f"{stage_name}: {Path(path).name} RGB rows = {len(rows)}")
        self.log(f"{stage_name}: exact RGB 100/100/100 rows = {exact_white}; exact RGB 0/0/0 rows = {exact_black}")
        self.log(f"{stage_name}: nearest white: {self._fmt_rgb_row(nearest_white)}")
        self.log(f"{stage_name}: max RGB sum:    {self._fmt_rgb_row(max_sum)}")
        self.log(f"{stage_name}: nearest black: {self._fmt_rgb_row(nearest_black)}")
        self.log(f"{stage_name}: min RGB sum:    {self._fmt_rgb_row(min_sum)}")

        if nearest_white is None:
            self.log(f"WARNING: {Path(path).name} contains no parseable RGB rows.")
        else:
            nw_max = max(nearest_white["r"], nearest_white["g"], nearest_white["b"])
            nw_avg = (nearest_white["r"] + nearest_white["g"] + nearest_white["b"]) / 3.0
            if nw_max < 85 or nw_avg < 80:
                self.log(
                    f"WARNING: nearest white in {Path(path).name} is relatively dark "
                    f"(average RGB {nw_avg:.2f}).  Check targen/printtarg settings and chart alignment."
                )
            elif exact_white < 1:
                self.log(
                    f"NOTE: {Path(path).name} contains no literal RGB 100/100/100 row. "
                    "This can be normal for printtarg output; using nearest-white diagnostics instead."
                )

        if measured and nearest_white is not None and "LAB_L" in nearest_white and nearest_white["LAB_L"] < 85:
            self.log(
                f"WARNING: measured nearest-white L* is only {nearest_white['LAB_L']:.2f}. "
                "This may indicate a bad or misaligned chartread pass."
            )

        return {
            "rows": len(rows),
            "exact_white": exact_white,
            "exact_black": exact_black,
            "nearest_white": nearest_white,
            "nearest_black": nearest_black,
            "max_sum": max_sum,
            "min_sum": min_sum,
        }

    def max_lab_l_for_rgb_white(self, path):
        """Return the maximum LAB_L among exact RGB white rows, or None if unavailable.

        Kept for compatibility with older code paths; endpoint diagnostics now use
        nearest-white rather than requiring an exact RGB 100/100/100 row.
        """
        best = None
        try:
            rows = self._rgb_rows_from_cgats(path)
        except Exception:
            return None

        for row in rows:
            if "LAB_L" not in row:
                continue
            if abs(row["r"] - 100.0) < 0.0001 and abs(row["g"] - 100.0) < 0.0001 and abs(row["b"] - 100.0) < 0.0001:
                best = row["LAB_L"] if best is None else max(best, row["LAB_L"])

        return best

    def require_rgb_white_rows(self, path, stage_name, measured=False):
        """Compatibility wrapper: log endpoint diagnostics, but do not hard-fail.

        The old name is intentionally retained so existing call sites keep working.
        Absence of a literal RGB 100/100/100 row is no longer fatal.
        """
        diag = self.rgb_endpoint_diagnostic(path, stage_name, measured=measured)
        return diag.get("exact_white", 0)

    def remove_zero_byte_profiles(self, basename, working_dir):
        """Remove bogus zero-byte profile files left by failed colprof runs."""
        for ext in (".icc", ".icm"):
            p = working_dir / f"{basename}{ext}"
            try:
                if p.exists() and p.stat().st_size == 0:
                    p.unlink()
                    self.log(f"Removed zero-byte failed profile: {p.name}")
            except Exception as e:
                self.log(f"WARNING: Could not remove {p.name}: {e}")


    def _unique_existing_paths(self, paths):
        """Return unique existing paths, preserving order."""
        seen = set()
        existing = []
        for path in paths:
            try:
                p = Path(path)
            except Exception:
                continue
            key = str(p.resolve()) if p.exists() else str(p)
            if p.exists() and key not in seen:
                seen.add(key)
                existing.append(p)
        return existing

    def _candidate_files_for_step(self, step_num, basename):
        """Return files that a step may overwrite or make stale.

        This deliberately includes downstream products as a warning, because
        regenerating a target or print target invalidates later files even if
        the command does not literally overwrite them.
        """
        working_dir = self.get_working_dir()
        paths = []

        # Files in the working directory using the operational basename.
        ti1 = working_dir / f"{basename}.ti1"
        ti2 = working_dir / f"{basename}.ti2"
        ti3 = working_dir / f"{basename}.ti3"
        icc = working_dir / f"{basename}.icc"
        icm = working_dir / f"{basename}.icm"
        print_files = []
        for pattern in (f"{basename}*.ps", f"{basename}*.eps", f"{basename}*.tif", f"{basename}*.tiff"):
            print_files.extend(sorted(working_dir.glob(pattern)))

        if step_num == 1:
            # A new targen run makes all later products stale.
            paths.extend([ti1, ti2, ti3, icc, icm])
            paths.extend(print_files)
        elif step_num == 2:
            # A new printtarg run overwrites .ti2/print files and invalidates later products.
            paths.extend([ti2, ti3, icc, icm])
            paths.extend(print_files)
        elif step_num == 3:
            # A new chartread run overwrites .ti3 and invalidates later profile products.
            paths.extend([ti3, icc, icm])
        elif step_num == 4:
            # A new colprof run overwrites the working profile and final installed copy.
            paths.extend([icc, icm])
            try:
                printer = self.vars['printer_name'].get()
                paper = self.vars['paper_name'].get()
                ink = self.vars['ink_name'].get()
                output_profile = f"{printer}_{paper}_{ink}.icc"
                output_dir = Path(os.path.expanduser(self.vars['output_dir'].get()))
                paths.append(output_dir / output_profile)
            except Exception:
                pass

        return self._unique_existing_paths(paths)

    def confirm_overwrite_for_step(self, step_num, basename):
        """Ask before overwriting or invalidating existing generated files."""
        existing = self._candidate_files_for_step(step_num, basename)
        if not existing:
            return True

        names = []
        for p in existing[:12]:
            try:
                names.append(str(p.relative_to(self.get_working_dir())))
            except Exception:
                names.append(str(p))
        if len(existing) > 12:
            names.append(f"... and {len(existing) - 12} more")

        msg = (
            f"Step {step_num} may overwrite or invalidate existing generated file(s):\n\n"
            + "\n".join(names)
            + "\n\nContinue?\n\n"
            "Choose No if these files correspond to a target you have already printed or measured."
        )
        return self.ask_yes_no("Existing files found", msg)


    # === Preconditioning safety helpers ===

    def _precond_profile_value(self):
        """Return a real selected preconditioning profile path for warning checks, or empty for none/blank."""
        precond = (self.vars.get('precond_profile', tk.StringVar(value='')).get() or '').strip()
        if not precond or precond.lower() == 'none':
            return ''
        return precond

    def _looks_vendor_precond_profile(self, precond):
        """Heuristic for profiles that are risky as Argyll preconditioners.

        Preconditioning should describe the actual target-printing path.  In this
        workflow that normally means a locally generated Argyll/YAAW ICC from the
        same printer/ink/media setting.  Canned/vendor profiles — especially
        Canon profiles used while printing through TurboPrint — may describe a
        different driver colour pipeline and can mislead targen.
        """
        text = str(precond or '').lower()
        vendor_markers = [
            'canon',
            'epson',
            'hp_', '/hp', 'hewlett',
            'brother',
            'gutenprint',
            'cups',
            'vendor',
            'canned',
            'driver',
        ]
        return any(marker in text for marker in vendor_markers)

    def confirm_preconditioning_for_step1(self):
        """Warn before using a suspicious preconditioning profile."""
        precond = self._precond_profile_value()
        if not precond:
            return True

        self.log(f"Preconditioning profile selected: {precond}")
        self.log(
            "Preconditioning note: safest results come from a locally generated "
            "ICC for the same printer/ink/media/driver path. Vendor/canned ICCs "
            "may describe a different colour pipeline."
        )

        if not self._looks_vendor_precond_profile(precond):
            return True

        msg = (
            "The selected preconditioning profile looks like it may be a vendor/canned "
            "profile rather than a locally generated Argyll/YAAW profile:\n\n"
            f"{precond}\n\n"
            "For this workflow, preconditioning should normally use an ICC made from "
            "the same printer, ink, paper/media setting, and print pipeline.\n\n"
            "Canon or other driver-supplied profiles can describe a different colour "
            "separation pipeline and may cause poor target distributions or high ΔE "
            "chartread errors.\n\n"
            "Continue anyway?"
        )
        return self.ask_yes_no("Questionable preconditioning ICC", msg)

    def _snapshot_workflow_settings(self):
        """Return plain Python values for worker threads.

        Tcl/Tk variables must only be read on the Tk main thread.  Each workflow
        runner calls this before starting its worker, and the worker uses the
        resulting immutable dictionary for command construction and paths.
        """
        return {name: var.get() for name, var in self.vars.items()}

    @staticmethod
    def _working_dir_from_settings(settings, basename):
        """Resolve the working directory without touching Tk variables."""
        value = str(settings.get('working_dir', '') or '').strip()
        if value:
            return Path(os.path.expanduser(value))
        return WORKING_ROOT / strip_argyll_suffix(basename)

    # === Workflow Step Runners ===
    
    def run_step1(self):
        """Run Step 1: Generate Target"""
        if not self.validate_config():
            return
        
        if self.demo_mode:
            self.show_warning("Demo Mode", 
                "ArgyllCMS not installed. Cannot run profiling steps.")
            return
        
        settings = self._snapshot_workflow_settings()
        basename = settings['basename']
        if not self.confirm_preconditioning_for_step1():
            self.log("Step 1 cancelled; preconditioning profile not used.")
            return

        if not self.confirm_overwrite_for_step(1, basename):
            self.log("Step 1 cancelled; existing files preserved.")
            return

        self._set_details_available(False)
        self._activate_project_log(basename, "Step 1 - targen")
        self.save_session()
        self.save_project_config(log_message=True)
        
        def task():
            try:
                self._step1_generate_target(basename, settings)
                self._ui_call(self.save_session, last_step_completed=1)
            except Exception as e:
                self.log(f"ERROR: {e}")
                self.show_error("Error", str(e))
        
        threading.Thread(target=task, daemon=True).start()
    
    def run_step2(self):
        """Run Step 2: Print Target"""
        if not self.validate_config():
            return
        
        if self.demo_mode:
            self.show_warning("Demo Mode", 
                "ArgyllCMS not installed. Cannot run profiling steps.")
            return
        
        settings = self._snapshot_workflow_settings()
        basename = settings['basename']
        if not self.confirm_overwrite_for_step(2, basename):
            self.log("Step 2 cancelled; existing files preserved.")
            return

        self._set_details_available(False)
        self._activate_project_log(basename, "Step 2 - printtarg")
        self.save_session()
        self.save_project_config(log_message=True)
        
        def task():
            try:
                self._step2_print_target(basename, settings)
                self._ui_call(self.save_session, last_step_completed=2)
            except Exception as e:
                self.log(f"ERROR: {e}")
                self.show_error("Error", str(e))
        
        threading.Thread(target=task, daemon=True).start()
    
    def run_step3(self):
        """Run Step 3: Read Target"""
        if not self.validate_config():
            return
        
        if self.demo_mode:
            self.show_warning("Demo Mode", 
                "ArgyllCMS not installed. Cannot run profiling steps.")
            return
        
        settings = self._snapshot_workflow_settings()
        basename = settings['basename']

        # Instrument availability is the first Step 3 prerequisite.  Check it
        # before asking whether existing .ti3/profile files may be overwritten,
        # so a missing or mismatched device does not lead to an irrelevant prompt.
        instrument = normalise_instrument_code(settings.get('printtarg_instrument', 'CM'))
        working_dir = self._working_dir_from_settings(settings, basename)
        preflight_cwd = working_dir if working_dir.is_dir() else Path.home()
        try:
            self._preflight_chartread_instrument(instrument, preflight_cwd)
        except Exception as exc:
            self.set_status("Step 3 not started")
            self.log(f"Instrument preflight failed: {exc}")
            self.show_error("Instrument Check", str(exc))
            return

        if not self.confirm_overwrite_for_step(3, basename):
            self.log("Step 3 cancelled; existing files preserved.")
            return

        self._set_details_available(False)
        self._activate_project_log(basename, "Step 3 - chartread")
        self.save_session()
        self.save_project_config(log_message=True)
        
        def task():
            try:
                completed = self._step3_read_target(basename, settings)
                if completed:
                    self._ui_call(self.save_session, last_step_completed=3)
                else:
                    self._ui_call(self.save_session)
            except Exception as e:
                self.log(f"ERROR: {e}")
                self.show_error("Error", str(e))
        
        threading.Thread(target=task, daemon=True).start()
    
    def run_step4(self):
        """Run Step 4: Build Profile"""
        if not self.validate_config():
            return
        
        if self.demo_mode:
            self.show_warning("Demo Mode", 
                "ArgyllCMS not installed. Cannot run profiling steps.")
            return
        
        settings = self._snapshot_workflow_settings()
        basename = settings['basename']
        if not self.confirm_overwrite_for_step(4, basename):
            self.log("Step 4 cancelled; existing files preserved.")
            return

        self._set_details_available(False)
        self._activate_project_log(basename, "Step 4 - colprof/profcheck")
        self.save_session()
        self.save_project_config(log_message=True)
        
        def task():
            try:
                self._step4_build_profile(basename, settings)
                self._ui_call(self._set_details_available, True)
            except Exception as e:
                self._ui_call(self._set_details_available, False)
                self.log(f"ERROR: {e}")
                self.show_error("Error", str(e))

        threading.Thread(target=task, daemon=True).start()
    
    # === Workflow Step Implementations ===
    
    def _step1_generate_target(self, basename, settings):
        """Step 1: Generate test target file using targen"""
        self.set_status("Generating target...")
        self.log("=== STEP 1: Generating Target ===")

        working_dir = self._working_dir_from_settings(settings, basename)
        working_dir.mkdir(parents=True, exist_ok=True)

        patches = settings['patches']
        ink_limit = settings['ink_limit']
        grey_steps = settings['targen_grey_steps']
        neutral_steps = settings['targen_neutral_steps']
        neutral_emphasis = settings['targen_neutral_emphasis']
        dark_emphasis = settings['targen_dark_emphasis']
        white_patches = settings['targen_white_patches']
        black_patches = settings['targen_black_patches']
        
        cmd = [
            'targen',
            '-v',          # Verbose output
            '-d2',         # Printer RGB
            '-f', patches, # Number of patches
            '-G',          # Generate good spread
            '-e', white_patches,  # White patches
            '-B', black_patches,  # Black patches
            '-g', grey_steps,        # Grey axis steps
            '-n', neutral_steps,     # Neutral axis steps
            '-N', neutral_emphasis,  # Neutral emphasis
            '-V', dark_emphasis,     # Dark emphasis
            '-l', ink_limit          # Ink limit
        ]
        
        # Blank means no explicit -c option, so targen uses its normal default
        # device-space model. Any non-blank value is passed as the -c operand.
        # The literal Argyll operand "none" is therefore preserved as
        # "-c none"; only actual profile paths are checked for existence.
        precond = str(settings.get('precond_profile', '') or '').strip()
        if precond:
            precond_arg = os.path.expanduser(precond)
            if precond.casefold() != 'none' and not os.path.exists(precond_arg):
                raise Exception(
                    "Preconditioning profile does not exist:\n\n"
                    f"{precond}\n\n"
                    "Use an existing ICC/MPP profile path, enter 'none', or leave the field blank."
                )
            cmd.extend(['-c', precond_arg])

        self._add_extra_args(cmd, 'targen_extra_args', 'targen', settings.get('targen_extra_args', ''))
        
        cmd.append(basename)
        
        self._run_command(cmd, cwd=working_dir)

        ti1_file = working_dir / f"{basename}.ti1"
        white_rows = self.count_rgb_white_rows(ti1_file)
        self.log(f"Post-targen diagnostic: {ti1_file.name} RGB 100/100/100 rows = {white_rows}")
        if white_rows < 1:
            self.log("WARNING: .ti1 contains no explicit RGB white row. Step 2 will log .ti2 nearest-white diagnostics.")

        self.log(f"Target generated: {basename}.ti1")
        self.set_status("Step 1 complete")
    
    def _step2_print_target(self, basename, settings):
        """Step 2: Create printable TIF files using printtarg"""
        self.set_status("Creating print files...")
        self.log("=== STEP 2: Creating Print Files ===")

        working_dir = self._working_dir_from_settings(settings, basename)

        # Check if .ti1 file exists
        ti1_file = working_dir / f"{basename}.ti1"
        if not ti1_file.exists():
            raise Exception(
                f"Target file not found: {basename}.ti1\n\n" +
                "Please run Step 1 (Generate Target) first."
            )

        paper_size = settings['paper_size']
        printtarg_paper_size = printtarg_paper_size_arg(paper_size)
        imgtype_val = settings['printtarg_imgtype']
        use_hexagon = settings['printtarg_hexagon']
        instrument = settings['printtarg_instrument']

        patches = settings['patches']
        self.log(f"Expected layout: {patch_layout_note(patches, paper_size, settings.get('printtarg_instrument', 'CM'))}")
        
        cmd = [
            'printtarg',
            '-v',          # Verbose output
            '-i', instrument,  # Target instrument
            '-p', printtarg_paper_size,  # Paper size
            '-M', '6',     #6mm margins
        ]
        
        # Add output image type flag (default PS = no flag)
        if 'EPS' in imgtype_val:
            cmd.append('-e')
        elif 'TIFF 8-bit' in imgtype_val:
            cmd.extend(['-t', '300'])   # 8-bit TIFF at 300 DPI
        elif 'TIFF 16-bit' in imgtype_val:
            cmd.extend(['-T', '300'])   # 16-bit TIFF at 300 DPI
        # PS (Postscript) = no extra flag needed
        # (DPI value is embedded in the label string for display clarity; flag args above are authoritative)

        # Add hexagon/DD patches flag if selected
        if use_hexagon:
            cmd.append('-h')

        self._add_extra_args(cmd, 'printtarg_extra_args', 'printtarg', settings.get('printtarg_extra_args', ''))
        
        cmd.append(basename)
        
        self._run_command(cmd, cwd=working_dir)

        ti2_file = working_dir / f"{basename}.ti2"
        if not ti2_file.exists():
            raise Exception(f"printtarg did not create expected target file: {ti2_file.name}")
        self.require_rgb_white_rows(ti2_file, "Post-printtarg check")
        
        # Find all generated output files (PS, EPS, or TIFF depending on type)
        if 'TIFF' in imgtype_val:
            output_files = list(working_dir.glob(f"{basename}*.tif"))
            file_label = "TIF"
        elif 'EPS' in imgtype_val:
            output_files = list(working_dir.glob(f"{basename}*.eps"))
            file_label = "EPS"
        else:
            output_files = list(working_dir.glob(f"{basename}*.ps"))
            file_label = "PS"
        
        if not output_files:
            self.log(f"WARNING: No {file_label} files found")
        else:
            self.log(f"\n=== Generated {len(output_files)} {file_label} file(s) ===")
            for output_file in sorted(output_files):
                abs_path = output_file.resolve()
                self.log(f"  {abs_path}")
            self.log("")
        
        self.log("PRINT INSTRUCTIONS:")
        self.log("1. Print with NO color management")
        self.log("2. Use proposed quality print settings")
        self.log("3. Allow prints to dry completely (24 hours recommended)")
        self.log("4. Proceed to Step 3 when ready to measure")
        self.set_status("Step 2 complete - PRINT NOW")
        
        # Open all output files with default viewer for printing
        for output_file in sorted(output_files):
            self._open_file_for_viewing(output_file)
    
    def _open_file_for_viewing(self, filepath):
        """Open a generated target with the platform default file opener.

        Keep this dependency-free.  Do not require ImageMagick/display or any
        specific image viewer.  Let the operating system route PS/EPS/TIF files
        to whatever application the user has configured for printing/viewing.
        """
        path = Path(filepath).expanduser()
        filepath = str(path)
        self.log(f"Opening: {filepath}")

        open_commands = []

        if sys.platform == 'darwin':
            # macOS: use LaunchServices/default app association.
            open_commands.append(['open', filepath])
        elif os.name == 'nt':
            # Not a primary target, but harmless if someone tries it.
            try:
                os.startfile(filepath)  # type: ignore[attr-defined]
                self.log("  Opened with: os.startfile")
                return
            except Exception as e:
                self.log(f"  WARNING: os.startfile failed: {e}")
        else:
            # Linux/*nix primary path: xdg-open is the freedesktop standard.
            # gio is a common fallback on GNOME-ish systems.
            open_commands.extend([
                ['xdg-open', filepath],
                ['gio', 'open', filepath],
                ['kde-open5', filepath],
                ['kde-open', filepath],
                ['exo-open', filepath],
            ])

        for cmd in open_commands:
            if shutil.which(cmd[0]) is None:
                continue
            try:
                subprocess.Popen(
                    cmd,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True,
                    close_fds=True,
                )
                self.log(f"  Opened with: {' '.join(cmd[:-1]) if len(cmd) > 1 else cmd[0]}")
                return
            except Exception as e:
                self.log(f"  WARNING: Could not open with {cmd[0]}: {e}")

        self.log("  Could not automatically open file")
        self.log(f"  Please manually open: {filepath}")
        self.show_info(
            "Manual Open Required",
            f"Could not automatically open the generated target file.\n\n"
            f"Please manually open this file to print:\n\n{filepath}\n\n"
            "The file is ready for printing."
        )
    
    @staticmethod
    def _instrument_family_matches(selected, description):
        """Return whether an Argyll device description matches YAAW's selection.

        Argyll's wording varies slightly by release and OEM branding, so compare
        normalised family aliases rather than requiring one exact display name.
        """
        selected = normalise_instrument_code(selected)
        text = re.sub(r'[^a-z0-9]+', ' ', str(description or '').lower()).strip()
        compact = text.replace(' ', '')

        aliases = {
            'CM': (
                'colormunki', 'color munki', 'i1studio', 'i1 studio',
            ),
            'i1': (
                'i1pro', 'i1 pro', 'eyeone pro', 'eye one pro',
                'efi es1000', 'efi es2000',
            ),
            '3p': (
                'i1pro3', 'i1 pro 3', 'i1pro 3', 'i1 pro3',
                'efi es3000',
            ),
        }
        for alias in aliases.get(selected, (selected,)):
            alias_text = re.sub(r'[^a-z0-9]+', ' ', alias.lower()).strip()
            if alias_text in text or alias_text.replace(' ', '') in compact:
                # Do not let the broad i1/i1Pro family claim an i1Pro3.
                if selected == 'i1' and ('i1pro3' in compact or 'es3000' in compact):
                    continue
                return True
        return False

    def _preflight_chartread_instrument(self, selected, cwd):
        """Use ``chartread -?`` to verify a suitable instrument is connected.

        ArgyllCMS documents its usage output as the instrument/port discovery
        interface.  Known numbered device lines are parsed here.  A definite
        empty or mismatched list aborts Step 3 before its interactive terminal
        opens.  Unrecognised output is logged and allowed through so a future
        Argyll wording change cannot unnecessarily disable chartread.
        """
        selected = normalise_instrument_code(selected)
        chartread = shutil.which('chartread') or 'chartread'
        self.set_status("Checking measurement instrument...")
        self.log(f"Checking for selected instrument: {instrument_label(selected)}")

        try:
            result = subprocess.run(
                [chartread, '-?'],
                cwd=str(cwd),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                errors='replace',
                timeout=20,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise Exception(
                "Instrument check timed out while ArgyllCMS was scanning communication ports.\n\n"
                "Check that the selected spectrophotometer is connected and available, "
                "then try Step 3 again."
            ) from exc
        except OSError as exc:
            raise Exception(f"Could not run chartread instrument check: {exc}") from exc

        output = result.stdout or ''
        devices = []
        # Typical Argyll forms include:  1 = 'X-Rite ColorMunki ...'
        # Accept quoted and unquoted variants while avoiding ordinary usage lines.
        patterns = (
            re.compile(r"^\s*(\d+)\s*=\s*['\"](.+?)['\"]\s*$"),
            re.compile(r"^\s*(\d+)\s*=\s*(.+?)\s*$"),
        )
        for raw_line in output.splitlines():
            for pattern in patterns:
                match = pattern.match(raw_line)
                if match:
                    description = match.group(2).strip()
                    if description and (match.group(1), description) not in devices:
                        devices.append((match.group(1), description))
                    break

        if devices:
            descriptions = [description for _number, description in devices]
            self.log("ArgyllCMS detected: " + "; ".join(descriptions))
            if any(self._instrument_family_matches(selected, item) for item in descriptions):
                self.log(f"Instrument preflight passed for {instrument_label(selected)}.")
                return

            found = "\n".join(f"  {number}: {description}" for number, description in devices)
            raise Exception(
                f"The selected instrument is {instrument_label(selected)}, but ArgyllCMS did not "
                f"find a matching device.\n\nDetected instrument(s):\n{found}\n\n"
                "Connect the selected spectrophotometer, or change YAAW's Instrument setting, "
                "then run Step 3 again."
            )

        # Argyll releases use several explicit no-device phrasings.
        lowered = output.lower()
        no_device_markers = (
            'no instruments found', 'no instrument found',
            'no devices found', 'no device found',
            'no ports found', 'no serial ports found',
            'no usb instruments', 'no usb devices',
        )
        if any(marker in lowered for marker in no_device_markers):
            raise Exception(
                f"No measurement instrument was detected for Step 3.\n\n"
                f"Selected instrument: {instrument_label(selected)}\n\n"
                "Connect and power the spectrophotometer, confirm that macOS/Linux has made it "
                "available to ArgyllCMS, and then try again."
            )

        # A normal usage listing contains the -c discovery heading.  If Argyll
        # produced that heading but no numbered device entries, treat it as an
        # authoritative empty list.
        if ('set communication port from the following list' in lowered or
                'communication port from the following list' in lowered):
            raise Exception(
                f"ArgyllCMS did not list any connected measurement instrument.\n\n"
                f"Selected instrument: {instrument_label(selected)}\n\n"
                "Connect the spectrophotometer and try Step 3 again."
            )

        # Avoid a false refusal if a future/platform-specific Argyll build changes
        # the usage format.  chartread itself remains the final authority.
        self.log(
            "WARNING: ArgyllCMS instrument discovery output was not recognised; "
            "continuing to chartread for compatibility."
        )

    def _step3_read_target(self, basename, settings):
        """Step 3: Read printed target with the selected instrument using chartread"""
        self.set_status("Preparing to read target...")
        self.log("=== STEP 3: Reading Target ===")

        working_dir = self._working_dir_from_settings(settings, basename)
        abs_wd = working_dir.resolve()

        # Check if .ti1 file exists
        ti1_file = working_dir / f"{basename}.ti1"
        if not ti1_file.exists():
            raise Exception(
                f"Target file not found: {basename}.ti1\n\n" +
                "Please run Step 1 (Generate Target) first."
            )
        
        # Check if print target files exist (PS, EPS or TIF depending on setting)
        imgtype_val = settings['printtarg_imgtype']
        if 'TIFF' in imgtype_val:
            print_files = list(working_dir.glob(f"{basename}*.tif"))
            file_desc = "TIF"
        elif 'EPS' in imgtype_val:
            print_files = list(working_dir.glob(f"{basename}*.eps"))
            file_desc = "EPS"
        else:
            print_files = list(working_dir.glob(f"{basename}*.ps"))
            file_desc = "PS"
        if not print_files:
            raise Exception(
                f"Print files not found: {basename}*.{file_desc.lower()}\n\n"
                "Please run Step 2 (Print Target) first."
            )

        self.log("Follow ColorMunki on-screen instructions")
        self.log("Move slowly with steady pressure")
        self.log("")
        self.log("chartread will open in a YAAW measurement window.")
        self.log("Its complete output, including warnings and rereads, will also be recorded here.")
        self.log(f"Working directory: {abs_wd}")
        self.log("")

        threshold = settings['chartread_threshold']
        cie_val = settings['chartread_cie']
        highres = settings['chartread_highres']
        resume = settings.get('chartread_resume', False)
        supwrn = settings['chartread_supwrn']
        patch_by_patch = settings.get('chartread_patch_by_patch', False)
        instrument = normalise_instrument_code(settings.get('printtarg_instrument', 'CM'))

        cmd = [
            'chartread',
            '-v',              # Verbose output
            '-T', threshold,   # Patch consistence threshold
        ]

        # CIE save mode: default (no flag) = XYZ, -l = Lab, -L = both
        if 'Lab (-l)' in cie_val:
            cmd.append('-l')
        elif 'Both' in cie_val:
            cmd.append('-L')
        # 'XYZ (default)' → no flag

        # High resolution spectrum mode.
        # YAAW defaults -H to CM/ColorMunki only.  For i1/i1Pro and 3p/i1Pro3+,
        # omit -H unless the user explicitly adds it in Additional chartread Args.
        if highres and instrument == 'CM':
            cmd.append('-H')
        elif highres and instrument != 'CM':
            self.log(f"Note: chartread -H omitted for {instrument}; add -H to Additional chartread Args to force it.")

        # Resume a partly read chart.
        if resume:
            cmd.append('-r')

        # Suppress warnings mode.
        if supwrn:
            cmd.append('-S')

        # Read patches individually rather than by strip.
        if patch_by_patch:
            cmd.append('-p')

        self._add_extra_args(cmd, 'chartread_extra_args', 'chartread', settings.get('chartread_extra_args', ''))

        cmd.append(basename)

        # Prefer YAAW's own pseudo-terminal window so the complete interactive
        # session is visible and retained in the project log.  If PTY support is
        # unavailable, _run_interactive_command() falls back to the established
        # external-terminal launcher and returns before that detached session ends.
        completed_in_yaaw = self._run_interactive_command(cmd, cwd=working_dir)

        ti3_file = working_dir / f"{basename}.ti3"
        if ti3_file.exists() and ti3_file.stat().st_size > 0:
            self.require_rgb_white_rows(ti3_file, "Post-chartread check", measured=True)
            self.log(f"Measurement complete: {basename}.ti3")
            self.set_status("Step 3 complete")
            return True

        if completed_in_yaaw:
            raise Exception(
                f"chartread exited without creating a usable {ti3_file.name}. "
                "Review the Step 3 transcript above for warnings or errors."
            )

        self.log(
            f"chartread is running for {basename} in an external terminal fallback. "
            f"After it exits, continue to Step 4; YAAW will validate {ti3_file.name} then."
        )
        self.set_status("Step 3 running - complete chartread in external terminal")
        return False
    
    def _step4_build_profile(self, basename, settings):
        """Step 4: Build ICC profile using colprof"""
        self.set_status("Building ICC profile...")
        self.log("=== STEP 4: Building ICC Profile ===")

        working_dir = self._working_dir_from_settings(settings, basename)

        # Check if .ti3 measurement file exists
        ti3_file = working_dir / f"{basename}.ti3"
        if not ti3_file.exists():
            raise Exception(
                f"Measurement file not found: {basename}.ti3\n\n" +
                "Please run Step 3 (Read Target) first."
            )

        # The output ICC copy should preserve the operational Argyll basename,
        # including -Argyll_<patchcount>.  The working directory omits that suffix,
        # but the copied profile filename must not, otherwise 210/420/etc. runs
        # overwrite each other in ~/.local/share/color/icc.
        output_profile = f"{basename}.icc"

        # Use colprof metadata fields if filled, else fall back to auto-values
        desc = settings['colprof_description'] or settings['profile_desc']
        manufacturer = settings['colprof_manufacturer']
        model = settings['colprof_model']
        copyright_str = settings['colprof_copyright']

        # Extract single-letter codes from the dropdown values (e.g. "r - Rel. Colorimetric" -> "r")
        intent_code = settings['colprof_intent'][0]
        quality_code = settings['colprof_quality'][0]
        avgdev = settings['colprof_avgdev']

        cmd = [
            'colprof',
            '-v',                  # Verbose output
            '-D', desc,            # Profile description
            '-q', quality_code,    # Quality
            '-r', avgdev,          # Average deviation
            '-cmt',                # Copyright tag
            '-dpp',                # Use printer profile class
            '-Z', intent_code,     # Default rendering intent
        ]

        # Add optional metadata if provided
        if manufacturer:
            cmd.extend(['-A', manufacturer])
        if model:
            cmd.extend(['-M', model])
        if copyright_str:
            cmd.extend(['-C', copyright_str])

        # Add rendering profile if specified
        rendering_profile = settings['rendering_profile']
        if rendering_profile:
            cmd.extend(['-S', rendering_profile])

        self._add_extra_args(cmd, 'colprof_extra_args', 'colprof', settings.get('colprof_extra_args', ''))

        cmd.append(basename)

        self.require_rgb_white_rows(ti3_file, "Pre-colprof check", measured=True)
        self.remove_zero_byte_profiles(basename, working_dir)

        try:
            self._run_command(cmd, cwd=working_dir)
        except Exception:
            self.remove_zero_byte_profiles(basename, working_dir)
            raise

        # Run profcheck to validate the profile.  Keep the established compact
        # summary in the main Execution display, then capture Graeme Gill's
        # recommended verbose sorted/worst-patch view for the persistent logfile
        # only.  Python performs the ten-line truncation; no external head command
        # is invoked.
        self.log("\nValidating profile with profcheck...")
        cmd = ['profcheck', '-k', f'{basename}.ti3', f'{basename}.icc']
        self._run_command(cmd, cwd=working_dir)

        detailed_cmd = [
            'profcheck', '-v2', '-s', '-w', '-x',
            f'{basename}.ti3', f'{basename}.icc'
        ]
        self._run_command_head_to_project_log(
            detailed_cmd,
            cwd=working_dir,
            max_lines=10,
            quota_exempt_prefixes=("No of test patches",),
            heading="profcheck highest delta-E results (10 entries; X3DOM generated with Lab axes):"
        )

        # Copy profile to output directory
        output_dir = Path(os.path.expanduser(settings['output_dir']))
        output_dir.mkdir(parents=True, exist_ok=True)

        import shutil
        src = working_dir / f"{basename}.icc"
        dst = output_dir / output_profile
        shutil.copy(src, dst)

        self.log("")
        self.log("=== PROFILE CREATED SUCCESSFULLY ===")
        project_json = self._ui_call_wait(self.save_project_config, log_message=False)
        self.log(f"Profile: {output_profile}")
        self.log(f"Location: {dst}")
        if project_json:
            self.log(f"Project config: {project_json}")
        run_log = getattr(self, 'run_log_file', None)
        if run_log:
            self.log(f"Run log: {run_log}")
        self.log("")
        self.log("For system-wide installation, copy to:")
        self.log("  Linux: /usr/share/color/icc/")
        self.log("  macOS: ~/Library/ColorSync/Profiles/")
        self.log("  Windows: C:\\Windows\\System32\\spool\\drivers\\color\\")

        self.set_status("Complete! Profile created")

        # Clean up session file
        try:
            self.config_file.unlink()
        except Exception:
            pass

        success_msg = f"Profile created successfully!\n\n{output_profile}\n\nSaved to: {dst}"
        if project_json:
            success_msg += f"\n\nConfig saved to: {project_json}"
        run_log = getattr(self, 'run_log_file', None)
        if run_log:
            success_msg += f"\nRun log: {run_log}"
        self.show_info("Success", success_msg)
    
    # === Command Execution Helpers ===
    
    @staticmethod
    def _clean_terminal_text(text):
        """Remove terminal-only control sequences while preserving useful text."""
        # CSI sequences cover the colour/cursor controls emitted by Argyll and
        # common shells.  Keep tabs/newlines and discard other C0 controls.
        text = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', text)
        text = re.sub(r'\x1b\][^\x07]*(?:\x07|\x1b\\)', '', text)
        return ''.join(ch for ch in text if ch in '\n\r\t' or ord(ch) >= 32)

    def _log_stream_chunks(self, chunks, prefix=''):
        """Convert a byte/text stream into readable log lines.

        Argyll progress meters commonly terminate each percentage with carriage
        return rather than newline.  Treat those carriage returns as spaces so
        0%..100% remains one compact line instead of one hundred log entries.
        """
        pending = ''
        for chunk in chunks:
            pending += self._clean_terminal_text(chunk)
            while True:
                nl = pending.find('\n')
                cr = pending.find('\r')
                positions = [pos for pos in (nl, cr) if pos >= 0]
                if not positions:
                    break
                pos = min(positions)
                separator = pending[pos]
                piece = pending[:pos]
                pending = pending[pos + 1:]
                if separator == '\r':
                    # CR progress updates belong on one compact logical line.
                    pending = piece.rstrip() + ' ' + pending.lstrip()
                else:
                    self.log(f"{prefix}{piece.rstrip()}" if piece.strip() else '')
        if pending.strip():
            self.log(f"{prefix}{pending.rstrip()}")

    def _log_project_only(self, message):
        """Append a message to the persistent project log without displaying it.

        This is used for supplementary diagnostics that are valuable in the
        audit trail but would add clutter to the normal Execution display.
        """
        log_file = getattr(self, 'run_log_file', None)
        if not log_file or getattr(self, '_run_log_failed', False):
            return
        try:
            text = str(message)
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(log_file, 'a', encoding='utf-8') as f:
                for line in text.splitlines() or ['']:
                    f.write(f"[{ts}] {line}\n")
        except Exception:
            # As with log(), a supplementary audit-log failure must not abort
            # an otherwise successful profiling run.
            self._run_log_failed = True

    def _run_command_head_to_project_log(
        self, cmd, cwd=None, max_lines=10, heading=None, quota_exempt_prefixes=()
    ):
        """Run a command and write a compact leading selection to the project log.

        stdout and stderr are combined to match YAAW's normal command handling.
        ``max_lines`` limits ordinary result lines; lines beginning with one of
        ``quota_exempt_prefixes`` are retained without consuming that quota.
        The complete output is consumed in Python, avoiding a shell pipeline and
        any dependency on ``head``.
        """
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=cwd,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=False,
        )

        cleaned = self._clean_terminal_text(process.stdout or '')
        quota = max(0, int(max_lines))
        exempt_prefixes = tuple(str(prefix) for prefix in quota_exempt_prefixes)
        lines = []
        counted = 0
        for line in cleaned.splitlines():
            stripped = line.lstrip()
            is_exempt = bool(exempt_prefixes) and stripped.startswith(exempt_prefixes)
            if is_exempt:
                lines.append(line)
            elif counted < quota:
                lines.append(line)
                counted += 1
            else:
                break

        self._log_project_only('')
        if heading:
            self._log_project_only(heading)
        self._log_project_only(f"Running: {shlex.join(str(c) for c in cmd)}")
        for line in lines:
            self._log_project_only(line.rstrip())

        if process.returncode != 0:
            raise Exception(f"Command failed with code {process.returncode}")

    def _run_command(self, cmd, cwd=None):
        """Run a non-interactive command and retain readable combined output."""
        self.log(f"Running: {shlex.join(str(c) for c in cmd)}")

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=0,
            cwd=cwd
        )

        assert process.stdout is not None
        decoder = codecs.getincrementaldecoder('utf-8')('replace')

        def decoded_chunks():
            while True:
                data = process.stdout.read(4096)
                if not data:
                    tail = decoder.decode(b'', final=True)
                    if tail:
                        yield tail
                    break
                yield decoder.decode(data)

        self._log_stream_chunks(decoded_chunks())
        returncode = process.wait()
        if returncode != 0:
            raise Exception(f"Command failed with code {returncode}")

    def _create_chartread_window(self, title):
        """Create the lightweight terminal-like chartread display on Tk's thread."""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry('920x620')
        window.transient(self.root)

        outer = ttk.Frame(window, padding=8)
        outer.pack(fill='both', expand=True)
        ttk.Label(
            outer,
            text="chartread — type the requested key while this window has focus",
            anchor='w'
        ).pack(fill='x', pady=(0, 6))

        # Keep this interactive terminal widget platform-native.  In particular,
        # forcing a custom Text background caused keyboard focus/key delivery to
        # fail with some macOS Aqua/Tk combinations even though the window and
        # chartread prompt rendered normally.
        display = scrolledtext.ScrolledText(
            outer, wrap=tk.WORD, font=('TkFixedFont', 10), undo=False
        )
        display.pack(fill='both', expand=True)

        # Aqua may not honour focus_set() until the Toplevel has been mapped.
        # Apply it now and once more at idle time so Return and other chartread
        # control keys are reliably delivered to the PTY.
        display.focus_set()
        window.after_idle(display.focus_force)

        state = {'master_fd': None, 'process': None, 'closing': False}

        def send_key(event):
            fd = state.get('master_fd')
            if fd is None:
                return 'break'
            mapping = {
                'Return': b'\r', 'KP_Enter': b'\r', 'BackSpace': b'\x7f',
                'Tab': b'\t', 'Escape': b'\x1b'
            }
            data = mapping.get(event.keysym)
            if data is None and event.state & 0x4 and event.keysym.lower() == 'c':
                data = b'\x03'
            elif data is None and event.char:
                data = event.char.encode('utf-8', errors='ignore')
            if data:
                try:
                    os.write(fd, data)
                except OSError:
                    pass
            return 'break'

        def request_close():
            proc = state.get('process')
            if proc is not None and proc.poll() is None:
                if not self.ask_yes_no(
                    "Stop chartread?",
                    "chartread is still running. Stop the measurement session and close this window?"
                ):
                    return
                state['closing'] = True
                try:
                    os.write(state['master_fd'], b'\x03')
                except (OSError, TypeError):
                    try:
                        proc.send_signal(signal.SIGINT)
                    except Exception:
                        pass
                return
            window.destroy()

        display.bind('<KeyPress>', send_key)
        # Bind Return at the Toplevel as a macOS/Aqua fallback.  The display
        # binding remains the normal path; returning 'break' prevents a second
        # copy being inserted into the Text widget.
        window.bind('<Return>', send_key, add='+')
        window.bind('<KP_Enter>', send_key, add='+')
        window.protocol('WM_DELETE_WINDOW', request_close)
        return window, display, state

    def _ring_chartread_bells(self, count):
        """Replay BEL characters emitted by chartread using Tk's native bell.

        Argyll uses one bell for an accepted strip and two for a failed read.
        Scheduling each bell separately preserves that distinction without
        introducing a platform-specific sound player.
        """
        for index in range(min(max(int(count), 0), 6)):
            self.root.after(index * 140, self.root.bell)

    @staticmethod
    def _chartread_log_messages(record):
        """Return concise, operator-useful log messages from chartread output.

        The live measurement window intentionally shows the full transcript.
        The persistent project log instead keeps instrument/calibration facts
        and anything that looks like a warning, failed read, or error, while
        dropping the repeated key instructions and normal per-strip prompts.
        """
        text = re.sub(r'\s+', ' ', record or '').strip()
        if not text:
            return []

        messages = []

        # Retain the useful session header/instrument identity when present.
        if text.startswith('Steps in each Pass'):
            header = re.split(r'(?=Set instrument sensor|Ready to read strip pass)', text, maxsplit=1)[0].strip()
            if header:
                messages.append(header)
        elif 'Instrument Type:' in text:
            match = re.search(
                r'(Instrument Type:.*?)(?=Set instrument sensor|Calibration complete|Ready to read strip pass|$)',
                text
            )
            if match:
                messages.append(match.group(1).strip())

        if 'Calibration complete' in text:
            messages.append('Instrument calibration complete.')

        # Remove routine interactive boilerplate before looking for red flags.
        cleaned = text
        boilerplate = (
            r"Ready to read strip pass\s+\S+(?:\s+\(!! ALL ROWS READ !!\))?",
            r"Press 'f' to move forward, 'b' to move back, 'n' for next unread, "
            r"'d' when done, Esc or 'q' to quit without saving\.",
            r"Trigger instrument switch or any other key to start:",
            r"Strip read OK(?: \(Strip read in reverse direction\))?",
            r"Set instrument sensor to calibration position, and then hit any key to continue, "
            r"or hit Esc or Q to abort:",
        )
        for pattern in boilerplate:
            cleaned = re.sub(pattern, ' ', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip(' :')

        red_flag = re.compile(
            r'warning|error|fatal|failed|failure|misread|unexpected|wrong strip|'
            r'inconsistent|retry|unable|cannot|communication|calibration error',
            re.IGNORECASE
        )
        if cleaned and red_flag.search(cleaned):
            messages.append(cleaned)

        # Preserve order but avoid duplicate fragments from mixed CR/LF output.
        unique = []
        for message in messages:
            if message and message not in unique:
                unique.append(message)
        return unique

    def _run_chartread_pty(self, cmd, cwd=None):
        """Run chartread in a YAAW-owned Unix pseudo-terminal."""
        if os.name == 'nt' or not hasattr(os, 'openpty'):
            raise OSError("pseudo-terminal support is unavailable")

        window, display, state = self._ui_call_wait(
            self._create_chartread_window, "YAAW chartread"
        )
        master_fd, slave_fd = os.openpty()
        process = None

        def append_display(text):
            if not window.winfo_exists():
                return
            display.insert(tk.END, text)
            display.see(tk.END)

        def close_window():
            try:
                if window.winfo_exists():
                    window.destroy()
            except tk.TclError:
                pass

        try:
            process = subprocess.Popen(
                cmd,
                stdin=slave_fd,
                stdout=slave_fd,
                stderr=slave_fd,
                cwd=cwd,
                close_fds=True,
                start_new_session=True,
            )
            os.close(slave_fd)
            slave_fd = -1
            state['master_fd'] = master_fd
            state['process'] = process

            self.log(f"Running interactive: {shlex.join(str(c) for c in cmd)}")
            self.log("chartread log: routine prompts and successful strip reads are omitted; warnings and errors are retained.")
            decoder = codecs.getincrementaldecoder('utf-8')('replace')
            record_pending = ''
            logged_messages = set()
            red_flag_count = 0
            current_strip = None

            def process_log_record(record):
                nonlocal red_flag_count, current_strip
                strip_match = re.search(r'Ready to read strip pass\s+(\S+)', record or '', re.IGNORECASE)
                if strip_match:
                    current_strip = strip_match.group(1).strip('()')
                for message in self._chartread_log_messages(record):
                    if message in logged_messages:
                        continue
                    logged_messages.add(message)
                    if re.search(
                        r'warning|error|fatal|failed|failure|misread|unexpected|wrong strip|'
                        r'inconsistent|retry|unable|cannot|communication',
                        message,
                        re.IGNORECASE
                    ):
                        red_flag_count += 1
                        strip_context = f"Strip {current_strip}: " if current_strip else ""
                        self.log(f"CHARTREAD WARNING: {strip_context}{message}")
                    else:
                        self.log(message)

            while True:
                ready, _, _ = select.select([master_fd], [], [], 0.10)
                if ready:
                    try:
                        data = os.read(master_fd, 4096)
                    except OSError:
                        data = b''
                    if data:
                        decoded = decoder.decode(data)

                        # chartread emits BEL once for success and twice for a
                        # failed read. Replay the same count through Tk.
                        bell_count = decoded.count('\x07')
                        if bell_count:
                            self._ui_call(self._ring_chartread_bells, bell_count)

                        text = self._clean_terminal_text(decoded)
                        shown = text.replace('\r\n', '\n').replace('\r', ' ')
                        self._ui_call(append_display, shown)

                        # For chartread, CR and LF both delimit potential log
                        # records. Unlike progress meters, routine prompts are
                        # filtered rather than folded into one enormous line.
                        record_pending += text
                        parts = re.split(r'[\r\n]+', record_pending)
                        record_pending = parts.pop() if parts else ''
                        for part in parts:
                            process_log_record(part)
                    elif process.poll() is not None:
                        break
                elif process.poll() is not None:
                    break

            tail = decoder.decode(b'', final=True)
            if tail:
                bell_count = tail.count('\x07')
                if bell_count:
                    self._ui_call(self._ring_chartread_bells, bell_count)
                clean_tail = self._clean_terminal_text(tail)
                self._ui_call(append_display, clean_tail.replace('\r\n', '\n').replace('\r', ' '))
                record_pending += clean_tail
            if record_pending.strip():
                process_log_record(record_pending)

            returncode = process.wait()
            self._ui_call(append_display, f"\n[chartread exited with code {returncode}]\n")
            if returncode != 0 and not state.get('closing'):
                raise Exception(f"chartread failed with code {returncode}")

            if returncode == 0:
                if red_flag_count:
                    self.log(f"chartread completed with {red_flag_count} warning/error message(s); review the Step 3 entries above.")
                else:
                    self.log("chartread completed without recorded warnings or errors.")
                # Leave the exit indication visible momentarily, then restore
                # the pre-3.40.3 behaviour of closing automatically.
                self._ui_call(window.after, 650, close_window)
            return True
        finally:
            if slave_fd >= 0:
                try:
                    os.close(slave_fd)
                except OSError:
                    pass
            try:
                os.close(master_fd)
            except OSError:
                pass
            state['master_fd'] = None
            state['process'] = process

    def _run_interactive_command(self, cmd, cwd=None):
        """Run chartread internally, retaining external terminal fallback."""
        try:
            return self._run_chartread_pty(cmd, cwd=cwd)
        except (OSError, tk.TclError) as exc:
            # Fall back only when the PTY/window could not be established.
            # A real chartread non-zero exit is measurement evidence and must
            # be reported rather than silently launching a second session.
            self.log(f"WARNING: Internal chartread window unavailable: {exc}")

        cmd_str = shlex.join(str(c) for c in cmd)
        self.log(f"Launching external interactive fallback: {cmd_str}")
        if self.open_in_terminal("YAAW chartread", cmd_str, cwd=cwd, hold_open=False):
            return False

        self.show_warning(
            "No Interactive Terminal",
            "YAAW could not create its internal chartread window and no supported "
            "external terminal emulator was found."
        )
        raise Exception("No usable interactive terminal is available for chartread")


    # -------------------------------------------------------------------------
    # Gamut Viewer
    # -------------------------------------------------------------------------

    def show_gamut_viewer(self):
        """Run iccgamut on the current profile and display a*b*, L*a*, and L*b* projections."""
        import math

        working_dir = self.get_working_dir()
        basename    = self.vars.get('basename', tk.StringVar()).get().strip()

        if not basename:
            self.show_warning("Gamut Viewer", "No basename set — please configure a profile first.")
            return

        icc_path = working_dir / f"{basename}.icc"
        if not icc_path.exists():
            self.show_warning("Gamut Viewer",
                f"Profile not found:\n{icc_path}\n\nPlease complete Step 4 (Build Profile) first.")
            return

        # iccgamut derives every output filename from the supplied profile name.
        # Use a short-lived profile copy with a distinct stem so its gamut X3DOM
        # can never overwrite profcheck's <basename>.x3d.html error model.
        gamut_stem = f"{basename}-gamut"
        gamut_profile_path = working_dir / f"{gamut_stem}.icc"
        gam_path = working_dir / f"{gamut_stem}.gam"
        gamut_3d_path = working_dir / f"{gamut_stem}.x3d.html"

        # --- Run iccgamut to generate both the .gam hull and X3DOM model ---
        # -d 10 gives a reasonable surface resolution (1.0–50.0; lower = finer)
        # -w emits the rotatable X3DOM HTML model as well as the CGATS .gam file.
        try:
            shutil.copy2(icc_path, gamut_profile_path)
            result = subprocess.run(
                ['iccgamut', '-d', '10', '-w', str(gamut_profile_path)],
                capture_output=True, text=True, timeout=120, cwd=str(working_dir)
            )
            if result.returncode != 0:
                self.show_error("Gamut Viewer",
                    f"iccgamut failed (code {result.returncode}):\n{result.stderr[:600]}")
                return
        except FileNotFoundError:
            self.show_error("Gamut Viewer",
                "iccgamut not found.\n\nMake sure ArgyllCMS is installed and iccgamut is in your PATH.")
            return
        except subprocess.TimeoutExpired:
            self.show_error("Gamut Viewer", "iccgamut timed out — try again.")
            return
        except OSError as exc:
            self.show_error("Gamut Viewer",
                f"Could not prepare the independent gamut model:\n{exc}")
            return
        finally:
            try:
                gamut_profile_path.unlink()
            except OSError:
                pass

        if not gam_path.exists():
            self.show_error("Gamut Viewer",
                f"Gamut file not found after running iccgamut:\n{gam_path}\n\n"
                f"iccgamut output:\n{result.stdout[:400]}")
            return

        if not gamut_3d_path.exists():
            self.log(
                f"WARNING: iccgamut created {gam_path.name} but did not create "
                f"the expected X3DOM model {gamut_3d_path.name}."
            )

        # --- Parse the .gam file (CGATS format) ---
        # The file has two DATA sections:
        #   Section 1 — vertices: columns include LAB_L / LAB_A / LAB_B
        #                         (or JCh equivalents when -p j was used)
        #   Section 2 — triangle faces: columns VERTEX1 VERTEX2 VERTEX3
        # We parse BEGIN_DATA_FORMAT … END_DATA_FORMAT to find column indices
        # dynamically, so this works across all Argyll versions.
        vertices = []   # list of (L, a, b)
        faces    = []   # list of (i, j, k) — 0-based

        try:
            with open(gam_path, 'r') as fh:
                raw = fh.read()

            sections = []   # list of (col_names[], rows[])
            in_fmt = False; in_data = False
            cur_cols = []; cur_rows = []

            for line in raw.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line == 'BEGIN_DATA_FORMAT':
                    in_fmt = True; continue
                if line == 'END_DATA_FORMAT':
                    in_fmt = False; continue
                if line == 'BEGIN_DATA':
                    in_data = True; cur_rows = []; continue
                if line == 'END_DATA':
                    in_data = False
                    sections.append((list(cur_cols), list(cur_rows)))
                    continue
                if in_fmt:
                    cur_cols = line.split()
                    continue
                if in_data:
                    cur_rows.append(line.split())
                    continue

            if len(sections) < 1:
                raise ValueError("No CGATS DATA sections found.")

            # --- Section 1: vertices ---
            vcols, vrows = sections[0]
            # Accept LAB_L/LAB_A/LAB_B (Lab mode) or JCh_J/JCh_a/JCh_b (Jab mode)
            L_names = ['LAB_L', 'JCh_J', 'J', 'L']
            A_names = ['LAB_A', 'JCh_a', 'a', 'A']
            B_names = ['LAB_B', 'JCh_b', 'b', 'B']

            def find_col(cols, candidates):
                for c in candidates:
                    if c in cols:
                        return cols.index(c)
                # case-insensitive fallback
                lc = [x.upper() for x in cols]
                for c in candidates:
                    if c.upper() in lc:
                        return lc.index(c.upper())
                return None

            iL = find_col(vcols, L_names)
            iA = find_col(vcols, A_names)
            iB = find_col(vcols, B_names)

            if iL is None or iA is None or iB is None:
                # Last resort: assume columns 1,2,3 after SAMPLE_ID
                iL, iA, iB = 1, 2, 3

            for row in vrows:
                if len(row) > max(iL, iA, iB):
                    try:
                        vertices.append((float(row[iL]), float(row[iA]), float(row[iB])))
                    except ValueError:
                        pass

            # --- Section 2: faces (if present) ---
            if len(sections) >= 2:
                fcols, frows = sections[1]
                V1_names = ['VERTEX_0', 'VERTEX1', 'V1', 'v1', 'vertex1', 'vertex_0']
                V2_names = ['VERTEX_1', 'VERTEX2', 'V2', 'v2', 'vertex2', 'vertex_1']
                V3_names = ['VERTEX_2', 'VERTEX3', 'V3', 'v3', 'vertex3', 'vertex_2']
                i1 = find_col(fcols, V1_names)
                i2 = find_col(fcols, V2_names)
                i3 = find_col(fcols, V3_names)
                # Face rows have no leading index col — default to cols 0,1,2
                if i1 is None: i1, i2, i3 = 0, 1, 2
                for row in frows:
                    if len(row) > max(i1, i2, i3):
                        try:
                            # Argyll uses 0-based vertex indices — no adjustment needed
                            faces.append((int(row[i1]), int(row[i2]), int(row[i3])))
                        except ValueError:
                            pass

        except Exception as e:
            self.show_error("Gamut Viewer", f"Failed to parse gamut file:\n{e}")
            return

        if not vertices:
            # Show first 20 lines of the file to help diagnose
            try:
                with open(gam_path) as fh:
                    preview = "\n".join(fh.read().splitlines()[:25])
            except Exception:
                preview = "(could not read file)"
            self.show_error("Gamut Viewer",
                f"No vertex data found in gamut file.\n\n"
                f"Columns detected: {vcols if 'vcols' in dir() else 'none'}\n\n"
                f"File preview:\n{preview}")
            return

        # -----------------------------------------------------------------------
        # Convex hull helper (Andrew's monotone chain, pure stdlib)
        # -----------------------------------------------------------------------
        def _cross(O, A, B):
            return (A[0]-O[0])*(B[1]-O[1]) - (A[1]-O[1])*(B[0]-O[0])

        def convex_hull_2d(points):
            pts = sorted(set(points))
            if len(pts) < 3:
                return pts
            lower = []
            for p in pts:
                while len(lower) >= 2 and _cross(lower[-2], lower[-1], p) <= 0:
                    lower.pop()
                lower.append(p)
            upper = []
            for p in reversed(pts):
                while len(upper) >= 2 and _cross(upper[-2], upper[-1], p) <= 0:
                    upper.pop()
                upper.append(p)
            return lower[:-1] + upper[:-1]

        # -----------------------------------------------------------------------
        # Reference colour spaces (approximate a*b* convex hulls, L=50 cross-section)
        # -----------------------------------------------------------------------
        # Accurate sRGB and AdobeRGB a*b* gamut boundaries, derived from
        # real colorimetric primaries (IEC 61966-2-1 / D65) projected into L*a*b*,
        # then simplified with Ramer-Douglas-Peucker (ε=1.5) while preserving
        # correct convex winding order (shoelace area within ~1% of true value).
        # sRGB true a*b* area ≈ 23,054;  AdobeRGB ≈ 32,912 sq units.
        SRGB_AB = [
            (79,-108),(98,-61),(80,67),(-22,94),
            (-86,83),(-73,35),(-48,-14),(-20,-41),(11,-65),
        ]
        ADOBE_AB = [
            (-23,105),(-138,91),(-122,46),(-104,15),
            (-78,-21),(-4,-67),(80,-109),(105,-52),(90,75),
        ]

        # -----------------------------------------------------------------------
        # Metrics helpers
        # -----------------------------------------------------------------------
        def poly_area_2d(hull):
            n = len(hull)
            if n < 3: return 0.0
            area = 0.0
            for k in range(n):
                x0,y0 = hull[k]; x1,y1 = hull[(k+1)%n]
                area += x0*y1 - x1*y0
            return abs(area) / 2.0

        def gamut_volume(verts):
            """Exact volume via signed tetrahedra if faces available,
            prismatoid slice integration as fallback."""
            if faces:
                # Divergence theorem: V = (1/6) * |sum over triangles of
                # v0 . (v1 x v2)|  — exact for a closed oriented mesh
                total = 0.0
                for i0, i1, i2 in faces:
                    if max(i0,i1,i2) >= len(verts): continue
                    L0,a0,b0 = verts[i0]
                    L1,a1,b1 = verts[i1]
                    L2,a2,b2 = verts[i2]
                    total += (L0*(a1*b2 - a2*b1)
                             - a0*(L1*b2 - L2*b1)
                             + b0*(L1*a2 - L2*a1))
                return abs(total) / 6.0
            else:
                # Prismatoid fallback (~8% error)
                from collections import defaultdict
                bins = defaultdict(list)
                for L,a,b in verts:
                    key = round(L / 1.0) * 1.0
                    bins[key].append((a,b))
                levels = sorted(bins.keys())
                vol = 0.0
                prev_a, prev_L = None, None
                for lv in levels:
                    h = convex_hull_2d(bins[lv])
                    a = poly_area_2d(h)
                    if prev_a is not None:
                        am = (prev_a + a) / 2
                        vol += (lv - prev_L) * (prev_a + 4*am + a) / 6
                    prev_a, prev_L = a, lv
                return vol

        def hull_intersection_area(hull_a, hull_b, n_grid=200):
            """Monte-Carlo area of intersection of two convex polygons."""
            import random as _rnd
            _rnd.seed(0)
            all_x = [p[0] for p in hull_a+hull_b]
            all_y = [p[1] for p in hull_a+hull_b]
            xlo,xhi = min(all_x),max(all_x)
            ylo,yhi = min(all_y),max(all_y)
            box = (xhi-xlo)*(yhi-ylo)

            def in_hull(px,py,hull):
                n = len(hull)
                for k in range(n):
                    x0,y0=hull[k]; x1,y1=hull[(k+1)%n]
                    if (x1-x0)*(py-y0)-(y1-y0)*(px-x0) < 0:
                        return False
                return True

            hits = sum(
                1 for _ in range(n_grid*n_grid)
                if in_hull(
                    xlo + _rnd.random()*(xhi-xlo),
                    ylo + _rnd.random()*(yhi-ylo),
                    hull_a
                ) and in_hull(
                    xlo + _rnd.random()*(xhi-xlo),
                    ylo + _rnd.random()*(yhi-ylo),
                    hull_b
                )
            )
            return box * hits / (n_grid*n_grid)

        # -----------------------------------------------------------------------
        # Build projections from vertex cloud
        # -----------------------------------------------------------------------
        Ls = [v[0] for v in vertices]
        As = [v[1] for v in vertices]
        Bs = [v[2] for v in vertices]

        hull_ab = convex_hull_2d([(v[1], v[2]) for v in vertices])
        hull_La = convex_hull_2d([(v[1], v[0]) for v in vertices])
        hull_Lb = convex_hull_2d([(v[2], v[0]) for v in vertices])

        L_SLICES = [15, 30, 50, 70, 85]
        slice_hulls = []
        for lval in L_SLICES:
            band = [(v[1], v[2]) for v in vertices if abs(v[0] - lval) < 9]
            if len(band) >= 4:
                slice_hulls.append((lval, convex_hull_2d(band)))

        # -----------------------------------------------------------------------
        # Compute metrics
        # -----------------------------------------------------------------------
        vol          = gamut_volume(vertices)
        ab_area      = poly_area_2d(hull_ab)
        srgb_area    = poly_area_2d(SRGB_AB)
        adobe_area   = poly_area_2d(ADOBE_AB)
        chroma_max   = max(math.sqrt(a**2 + b**2) for _,a,b in vertices)
        black_pt     = min(Ls)
        white_pt     = max(Ls)
        # Coverage: profile a*b* area as % of reference (>100% = exceeds reference)
        srgb_cov     = ab_area / srgb_area * 100
        adobe_cov    = ab_area / adobe_area * 100
        # sRGB 3D Lab volume reference (IEC 61966-2-1, D65; matches ICCView ~899,155 cc)
        SRGB_VOL_REF = 899155.0
        srgb_vol_cov = vol / SRGB_VOL_REF * 100

        # -----------------------------------------------------------------------
        # Build the popup window
        # -----------------------------------------------------------------------
        PAD = 34

        # Keep the top a*b*/metrics panels square, but make the L*a*/L*b*
        # side views deliberately shallower.  Their L* axis spans only 0..100
        # while a*/b* commonly span well over 200 units, so square canvases make
        # the hulls look unnaturally tall and narrow.
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        width_limit = min(1440, screen_w - 60)
        height_limit = screen_h - 190
        CSIZE = max(300, min(560, (width_limit - 44) // 2,
                             int(height_limit / 1.66)))
        SIDE_HEIGHT = max(210, int(CSIZE * 0.58))

        win = tk.Toplevel(self.root)
        win.title(f"Gamut Viewer — {basename}.icc")
        win.resizable(True, True)

        import tkinter.font as tkfont
        axis_canvas_font = tkfont.Font(root=win, family='DejaVu Sans', size=11, weight='bold')
        tick_canvas_font = tkfont.Font(root=win, family='DejaVu Sans', size=9, weight='bold')
        guide_canvas_font = tkfont.Font(root=win, family='DejaVu Sans', size=9, weight='bold')
        ref_canvas_font = tkfont.Font(root=win, family='DejaVu Sans', size=9, weight='bold')

        ttk.Label(win, text=f"ICC Gamut: {basename}",
                  font=tick_canvas_font).pack(pady=(10, 2))

        top_frame = ttk.Frame(win)
        top_frame.pack(fill='both', expand=True, padx=10, pady=5)
        top_frame.columnconfigure(0, weight=1, uniform='gamut_top')
        top_frame.columnconfigure(1, weight=1, uniform='gamut_top')
        top_frame.rowconfigure(0, weight=1)

        # Top-left: a*b* view
        ab_frame = ttk.Frame(top_frame)
        ab_frame.grid(row=0, column=0, sticky='nsew')
        cv_ab = tk.Canvas(ab_frame, width=CSIZE, height=CSIZE, bg='#111418',
                          highlightthickness=1, highlightbackground='#444')
        cv_ab.pack(fill='both', expand=True)
        ttk.Label(ab_frame, text="a*b* plane  (top-down projection)",
                  foreground='gray').pack()

        # Top-right: metrics panel, deliberately the same footprint as a plot.
        mf = ttk.LabelFrame(top_frame, text="Profile Metrics", padding="14",
                            width=CSIZE, height=CSIZE)
        mf.grid(row=0, column=1, sticky='nsew', padx=(12, 0))
        mf.grid_propagate(False)

        metrics_body = ttk.Frame(mf)
        metrics_body.place(relx=0.5, rely=0.48, anchor='center')

        col1 = ttk.Frame(metrics_body); col1.pack(anchor='w', pady=(0, 10))
        col2 = ttk.Frame(metrics_body); col2.pack(anchor='w', pady=(0, 10))
        col3 = ttk.Frame(metrics_body); col3.pack(anchor='w')

        # Use dedicated fonts so the metrics remain comfortably readable as
        # the user enlarges the resizable viewer.  Font growth is deliberately
        # modest and capped so the panel stays tidy on very large displays.
        import tkinter.font as tkfont
        metrics_label_font = tkfont.Font(root=win, family='TkDefaultFont', size=11)
        metrics_value_font = tkfont.Font(root=win, family='TkDefaultFont', size=11, weight='bold')
        metrics_note_font = tkfont.Font(root=win, family='TkDefaultFont', size=9)

        def mrow(parent, label, value, note=''):
            f = ttk.Frame(parent); f.pack(anchor='w', pady=3)
            ttk.Label(f, text=label, width=18, anchor='w',
                      font=metrics_label_font).pack(side='left')
            ttk.Label(f, text=value, font=metrics_value_font).pack(side='left')
            if note:
                ttk.Label(f, text=f'  {note}', foreground='gray',
                          font=metrics_note_font).pack(side='left')

        mrow(col1, 'Gamut volume:',       f'{vol:,.0f}',    'cubic L*a*b*')
        mrow(col1, 'vs sRGB (area):',     f'{srgb_cov:.0f}%',      'of sRGB a*b* area')
        mrow(col1, 'vs sRGB (volume):',   f'{srgb_vol_cov:.0f}%',  'of sRGB 3D volume')
        mrow(col1, 'vs AdobeRGB:',        f'{adobe_cov:.0f}%',     'of AdobeRGB a*b* area')

        mrow(col2, 'Max chroma C*:',      f'{chroma_max:.1f}')
        mrow(col2, 'a* range:',           f'{min(As):.0f} to {max(As):.0f}')
        mrow(col2, 'b* range:',           f'{min(Bs):.0f} to {max(Bs):.0f}')

        mrow(col3, 'White point L*:',     f'{white_pt:.1f}')
        mrow(col3, 'Black point L*:',     f'{black_pt:.1f}')
        vol_method = 'exact' if faces else 'approx'
        mrow(col3, 'Vertices:',           f'{len(vertices)}')
        mrow(col3, 'Faces:',              f'{len(faces)}  ({vol_method} volume)')

        gamut_3d_button = ttk.Button(
            metrics_body,
            text="3D Gamut View",
            command=self.open_gamut_3d_model,
            style="YAAWAction.TButton"
        )
        gamut_3d_button.pack(anchor='center', pady=(14, 0))
        if not gamut_3d_path.exists():
            gamut_3d_button.state(['disabled'])

        def resize_metrics_text(event=None):
            try:
                panel_w = max(1, mf.winfo_width())
                panel_h = max(1, mf.winfo_height())
                # Baseline 11 pt at the normal viewer size, rising gradually
                # to 14 pt when the metrics panel is enlarged substantially.
                main_size = max(11, min(14, int(min(panel_w / 48, panel_h / 36))))
                note_size = max(9, main_size - 2)
                metrics_label_font.configure(size=main_size)
                metrics_value_font.configure(size=main_size)
                metrics_note_font.configure(size=note_size)
            except Exception:
                pass

        mf.bind('<Configure>', resize_metrics_text, add='+')
        win.after_idle(resize_metrics_text)

        # Legend.  Line samples show both colour and dash pattern, since
        # colour alone made the two reference spaces unnecessarily similar.
        leg = ttk.Frame(win)
        leg.pack(pady=(3, 0))
        legend_items = [
            ('#4fc3f7', None,   f'{basename}  '),
            ('#ff7043', (6, 3), 'sRGB  '),
            ('#b388ff', (2, 3), 'AdobeRGB  '),
            ('#6ec6a0', (2, 3), 'L* guides'),
        ]
        for colour, dash, label in legend_items:
            sample = tk.Canvas(leg, width=24, height=10,
                               highlightthickness=0, bg=win.cget('background'))
            sample.pack(side='left', padx=(6, 2))
            sample.create_line(1, 5, 23, 5, fill=colour, width=2, dash=dash)
            ttk.Label(leg, text=label, font=('TkDefaultFont', 8)).pack(side='left')

        # Bottom row: L*a* and L*b* side views
        bottom_frame = ttk.Frame(win)
        bottom_frame.pack(fill='both', expand=True, padx=10, pady=(6, 2))
        bottom_frame.columnconfigure(0, weight=1, uniform='gamut_bottom')
        bottom_frame.columnconfigure(1, weight=1, uniform='gamut_bottom')
        bottom_frame.rowconfigure(0, weight=1)

        cv_La = tk.Canvas(bottom_frame, width=CSIZE, height=SIDE_HEIGHT, bg='#111418',
                          highlightthickness=1, highlightbackground='#444')
        cv_La.grid(row=0, column=0, sticky='nsew', padx=(0, 8))
        ttk.Label(bottom_frame, text="L*a* plane  (side view, b* collapsed)",
                  foreground='gray').grid(row=1, column=0)

        cv_Lb = tk.Canvas(bottom_frame, width=CSIZE, height=SIDE_HEIGHT, bg='#111418',
                          highlightthickness=1, highlightbackground='#444')
        cv_Lb.grid(row=0, column=1, sticky='nsew')
        ttk.Label(bottom_frame, text="L*b* plane  (side view, a* collapsed)",
                  foreground='gray').grid(row=1, column=1)

        ttk.Button(win, text="Close", command=win.destroy).pack(pady=(5, 10))

        # -----------------------------------------------------------------------
        # Responsive drawing helpers
        # -----------------------------------------------------------------------
        def canvas_size(cv, fallback_w, fallback_h):
            cv.update_idletasks()
            width = max(220, cv.winfo_width() or fallback_w)
            height = max(170, cv.winfo_height() or fallback_h)
            return width, height

        def make_scaler(x_vals, y_vals, width, height, pad):
            ax = max(abs(min(x_vals)), abs(max(x_vals))) * 1.12 or 80
            ay = max(abs(min(y_vals)), abs(max(y_vals))) * 1.12 or 80
            draw_w = max(1, width - 2 * pad)
            draw_h = max(1, height - 2 * pad)
            scale = min(draw_w / (2 * ax), draw_h / (2 * ay))
            return scale, width / 2, height / 2

        def draw_grid(cv, scale, cx, cy, width, height, pad, xlabel, ylabel):
            # High-contrast plotting scaffold.  These labels must remain useful
            # on normal desktop displays, not merely decorative against the
            # dark canvas.
            grid_colour = '#66727a'
            axis_colour = '#ffffff'
            tick_colour = '#ffffff'
            text_colour = '#ffffff'
            axis_font = axis_canvas_font
            tick_font = tick_canvas_font

            for radius in (20, 40, 60, 80, 100):
                pr = radius * scale
                if pr < min(width, height) / 2 - pad:
                    cv.create_oval(cx-pr, cy-pr, cx+pr, cy+pr,
                                   outline=grid_colour, width=1)
            cv.create_line(pad, cy, width-pad, cy,
                           fill=axis_colour, width=3)
            cv.create_line(cx, pad, cx, height-pad,
                           fill=axis_colour, width=3)
            cv.create_text(width-pad+5, cy, text=xlabel,
                           fill=text_colour, anchor='w', font=axis_font)
            cv.create_text(cx, pad-5, text=ylabel,
                           fill=text_colour, anchor='s', font=axis_font)
            for value in range(-160, 161, 20):
                if value == 0:
                    continue
                px = cx + value * scale
                py = cy - value * scale
                if pad <= px <= width-pad:
                    cv.create_line(px, cy-5, px, cy+5,
                                   fill=tick_colour, width=3)
                    if value % 40 == 0:
                        cv.create_text(px, cy+15, text=str(value),
                                       fill=text_colour, font=tick_font,
                                       anchor='n')
                if pad <= py <= height-pad:
                    cv.create_line(cx-5, py, cx+5, py,
                                   fill=tick_colour, width=3)
                    if value % 40 == 0:
                        cv.create_text(cx-12, py, text=str(value),
                                       fill=text_colour, font=tick_font,
                                       anchor='e')

        def hull_to_canvas(hull_pts, scale, cx, cy):
            flat = []
            for x, y in hull_pts:
                flat += [cx + x * scale, cy - y * scale]
            return flat

        def draw_ref_ring(cv, ref_pts, scale, cx, cy, colour, dash):
            pts = hull_to_canvas(ref_pts, scale, cx, cy)
            pts += hull_to_canvas(ref_pts[:1], scale, cx, cy)
            cv.create_line(pts, fill=colour, width=2, dash=dash)

        def draw_ab_view():
            cv_ab.delete('all')
            width, height = canvas_size(cv_ab, CSIZE, CSIZE)
            scale, cx, cy = make_scaler(
                As + [a for a, b in ADOBE_AB] + [-80, 80],
                Bs + [b for a, b in ADOBE_AB] + [-80, 80],
                width, height, PAD)
            draw_grid(cv_ab, scale, cx, cy, width, height, PAD, 'a*', 'b*')

            if len(hull_ab) >= 3:
                cv_ab.create_polygon(
                    hull_to_canvas(hull_ab, scale, cx, cy),
                    fill='', outline='#4fc3f7', width=2)

            draw_ref_ring(cv_ab, ADOBE_AB, scale, cx, cy, '#b388ff', (2, 3))
            draw_ref_ring(cv_ab, SRGB_AB, scale, cx, cy, '#ff7043', (6, 3))
            draw_grid(cv_ab, scale, cx, cy, width, height, PAD, 'a*', 'b*')
            cv_ab.create_oval(cx-6, cy-6, cx+6, cy+6,
                              fill='white', outline='#d7dde1', width=2)
            cv_ab.create_text(cx+11, cy-11, text='D50', fill='#ffffff',
                              font=tick_canvas_font, anchor='sw')

        def draw_side_view(cv, hull_pts, x_vals, x_refs, xlabel, ref_label_getter):
            cv.delete('all')
            width, height = canvas_size(cv, CSIZE, SIDE_HEIGHT)

            # Reserve a label gutter so L* guide text never collides with
            # negative-axis reference markers at the left of the plot.
            left = 82
            right = 52
            top = 42
            bottom = 56
            x_extent = max(abs(min(x_vals + x_refs)),
                           abs(max(x_vals + x_refs))) * 1.12 or 80
            draw_w = max(1, width - left - right)
            draw_h = max(1, height - top - bottom)
            sx = draw_w / (2 * x_extent)
            sy = draw_h / 100.0
            cx = left + draw_w / 2
            y_bottom = height - bottom
            y_top = top

            def side_points(points):
                flat = []
                for x, lightness in points:
                    flat += [cx + x * sx, y_bottom - lightness * sy]
                return flat

            axis_colour = '#ffffff'
            tick_colour = '#ffffff'
            text_colour = '#ffffff'
            guide_colour = '#a8efc4'
            axis_font = axis_canvas_font
            tick_font = tick_canvas_font
            guide_font = guide_canvas_font

            cv.create_line(left, y_bottom, width-right, y_bottom,
                           fill=axis_colour, width=3)
            cv.create_line(cx, y_top, cx, y_bottom,
                           fill=axis_colour, width=3)
            cv.create_text(width-right+5, y_bottom, text=xlabel,
                           fill=text_colour, anchor='w', font=axis_font)
            cv.create_text(cx, y_top-5, text='L*', fill=text_colour,
                           anchor='s', font=axis_font)

            for value in range(-160, 161, 20):
                if value == 0:
                    continue
                px = cx + value * sx
                if left <= px <= width-right:
                    cv.create_line(px, y_bottom-5, px, y_bottom+5,
                                   fill=tick_colour, width=3)
                    if value % 40 == 0:
                        cv.create_text(px, y_bottom+14, text=str(value),
                                       fill=text_colour, font=tick_font,
                                       anchor='n')

            for lightness in range(0, 101, 20):
                py = y_bottom - lightness * sy
                cv.create_line(cx-5, py, cx+5, py,
                               fill=tick_colour, width=3)
                cv.create_text(cx-12, py, text=str(lightness),
                               fill=text_colour, font=tick_font, anchor='e')

            if len(hull_pts) >= 3:
                cv.create_polygon(side_points(hull_pts), fill='#0d2a3a',
                                  outline='#4fc3f7', width=2)

            for lval in L_SLICES:
                py = y_bottom - lval * sy
                cv.create_line(left, py, width-right, py,
                               fill=guide_colour, width=1, dash=(3, 4))
                cv.create_text(8, py, text=f'L*={lval}', fill='#c8f5db',
                               font=guide_font, anchor='w')

            references = [
                (ADOBE_AB, '#b388ff', (2, 3), 'AdobeRGB', 5),
                (SRGB_AB,  '#ff7043', (6, 3), 'sRGB', 19),
            ]
            for ref_pts, colour, dash, label, label_offset in references:
                x_min, x_max = ref_label_getter(ref_pts)
                for axis_val in (x_min, x_max):
                    px = cx + axis_val * sx
                    if left <= px <= width-right:
                        cv.create_line(px, y_bottom, px, y_top,
                                       fill=colour, width=2, dash=dash)
                px = cx + x_max * sx
                if left <= px <= width-right:
                    cv.create_text(px+3, y_top+label_offset, text=label,
                                   fill=colour,
                                   font=ref_canvas_font, anchor='sw')

            # Draw the plotting axes and labels last so the filled gamut hull
            # and reference lines cannot obscure them.
            cv.create_line(left, y_bottom, width-right, y_bottom,
                           fill=axis_colour, width=3)
            cv.create_line(cx, y_top, cx, y_bottom,
                           fill=axis_colour, width=3)
            cv.create_text(width-right+7, y_bottom-2, text=xlabel,
                           fill=text_colour, anchor='w', font=axis_font)
            cv.create_text(cx+7, y_top+2, text='L*', fill=text_colour,
                           anchor='sw', font=axis_font)

            for value in range(-160, 161, 20):
                if value == 0:
                    continue
                px = cx + value * sx
                if left <= px <= width-right:
                    cv.create_line(px, y_bottom-6, px, y_bottom+6,
                                   fill=tick_colour, width=3)
                    if value % 40 == 0:
                        cv.create_text(px, y_bottom+12, text=str(value),
                                       fill=text_colour, font=tick_font,
                                       anchor='n')

            for lightness in range(0, 101, 20):
                py = y_bottom - lightness * sy
                cv.create_line(cx-6, py, cx+6, py,
                               fill=tick_colour, width=3)
                cv.create_text(cx-14, py, text=str(lightness),
                               fill=text_colour, font=tick_font, anchor='e')

        def redraw_gamut(event=None):
            draw_ab_view()
            draw_side_view(
                cv_La, hull_La, As,
                [a for a, b in ADOBE_AB] + [a for a, b in SRGB_AB] + [-80, 80],
                'a*',
                lambda ref_pts: (min(a for a, b in ref_pts),
                                 max(a for a, b in ref_pts)))
            draw_side_view(
                cv_Lb, hull_Lb, Bs,
                [b for a, b in ADOBE_AB] + [b for a, b in SRGB_AB] + [-80, 80],
                'b*',
                lambda ref_pts: (min(b for a, b in ref_pts),
                                 max(b for a, b in ref_pts)))

        redraw_after_id = {'value': None}

        def queue_redraw(event=None):
            if redraw_after_id['value'] is not None:
                try:
                    win.after_cancel(redraw_after_id['value'])
                except Exception:
                    pass
            redraw_after_id['value'] = win.after(40, redraw_gamut)

        for canvas in (cv_ab, cv_La, cv_Lb):
            canvas.bind('<Configure>', queue_redraw, add='+')

        # Start at the former calculated size, but permit the user to enlarge
        # or reduce the viewer.  The plots redraw rather than merely exposing
        # blank space around fixed canvases.
        initial_w = min(screen_w - 40, max(900, 2 * CSIZE + 42))
        initial_h = min(screen_h - 70, max(700, CSIZE + SIDE_HEIGHT + 175))
        win.geometry(f'{initial_w}x{initial_h}')
        win.minsize(820, 620)
        win.after_idle(redraw_gamut)

# ---------------------------------------------------------------------------

def main():
    """Main entry point"""
    root = tk.Tk()
    app = PrinterProfilingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
