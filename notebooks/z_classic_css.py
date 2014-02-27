# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Run all cells in this notebook, then run IPython:
# N
# 
# ```
# $ ipython notebook --profile classic
# ```
# 
# Then remember to use ⌘-R to refresh your browser's cached css files

# <codecell>

profile_name = 'classic'

# <codecell>

!ipython profile create {profile_name}

# <codecell>

!ipython locate profile {profile_name}

# <codecell>

!mkdir ~/.ipython/profile_{profile_name}/static
!mkdir ~/.ipython/profile_{profile_name}/static/custom
!touch ~/.ipython/profile_{profile_name}/static/custom/custom.css

# <codecell>

%%file ~/.ipython/profile_{profile_name}/static/custom/custom.css
/*body {
    background: #073642;
    color: #839496;
}*/

div#notebook {
    border-top: 1px solid #586e75;
}

/* cell areas */
div.input_area {
    background: #DFDFDF;
    border: 1px solid #586e75;
}

div.text_cell_input {
    background: #EAEFF4 /*#002b36*/;
    border: 1px solid #586e75;

}

div.cell.selected {
    border-radius: 4px;
    border: thin black solid;
}

div.input_prompt {
    color: #93a1a1;
}

/* code cells */
.cm-s-ipython {
    background: #F7F7F7;
    color: black;
    font-family:  CONSOLAS, ANDALE MONO, COURIER;
    font-size: 14px;
}

div.cell.code_cell {  /* Areat containing both code and output */
color:black;
 background-color:#DFDFDF; /* light blue */
 border-radius: 0.4em; /* rounded borders = friendlier */
 padding: 1em;
 margin-top:2em;
}


/*
 *
 *  color: #859900;  // Dark Yellow
 *  color: #b58900;  // Strong Yellow
 *  color: #268bd2;  // Strong Blue
 *  color: #cb4b16;  // Strong Orange
 *  color: #586e75;  // Dark Grayish Cyan
 *  color: #2aa198;  // Dark Cyan
 *  color: #dc322f;  // Bright Red
 *  color: #839496;  // Dark Lighter Grayish Cyan
 */
.cm-s-ipython span.cm-keyword {
    color: #859900;
    font-weight: bold;
}
.cm-s-ipython span.cm-number {
    color: #268bd2;
}
.cm-s-ipython span.cm-operator {
    color: #b58900;
    font-weight: bold;
}
.cm-s-ipython span.cm-meta {
    color: #cb4b16;
}
.cm-s-ipython span.cm-comment {
    color: #586e75; 
    font-style: italic;
}
.cm-s-ipython span.cm-string {
    color: #2aa198;
}
.cm-s-ipython span.cm-error {
    color: #dc322f;
}
.cm-s-ipython span.cm-builtin {
    color: #cb4b16;
}
.cm-s-ipython span.cm-variable{
    color: #839496;
}

div.CodeMirror-cursor {
    border-left:solid 2px #93a1a1 !important;
}

div.CodeMirror-selected {
    background: #002B36 !important;
}

/* output area */
div.output_text pre{
    color: #839496;
    font-size:14px;
}

div.output_html {
    color: #839496;
}

/* text/markdown cells 
div.text_cell div {
    color: #839496;
}*/

div.text_cell code {
    background-color: transparent;
}

div.text_cell pre {
    background-color: transparent;
}

/* nav bar */
div.navbar-inner {
    background: #E6F1F6;
    border: 1px solid #586e75;
}

div.navbar-inner a {
    text-shadow: none !important;
}

div.navbar-inner a:hover {
    color: #839496 !important;
}

.notification_widget {
    background: none;
    border: 1px solid #586e75;
}

.btn {
    color: #2F3535;

    background-color: #E6F1F6 !important;
    background-image: linear-gradient(to bottom, #E6F1F6, #586e75);
    border: 1px solid #586e75;
    text-shadow: none;
}

.btn:hover {
    color: #2F3535;
}

select {
    color: #2F3535;
    background-color: #E6F1F6;
    background: gradient(none);
    border: 1px solid #586e75;
}

/* Notebooks interface */
.breadcrumb>li {
    text-shadow: none;
}
/*
.dropdown{
     background-color: #E6F1F6 !important;
    background-image: linear-gradient(to bottom, #E6F1F6, #586e75);
    /*border: 1px solid #586e75;*/
}


.dropdown:hover {
    color: #2F3535;
}*/

# <codecell>


