#!/bin/env python
#
# File: RDKitDrawMolecules.py
# Author: Manish Sud <msud@san.rr.com>
#
# Copyright (C) 2018 Manish Sud. All rights reserved.
#
# The functionality available in this script is implemented using RDKit, an
# open source toolkit for cheminformatics developed by Greg Landrum.
#
# This file is part of MayaChemTools.
#
# MayaChemTools is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.
#
# MayaChemTools is distributed in the hope that it will be useful, but without
# any warranty; without even the implied warranty of merchantability of fitness
# for a particular purpose.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with MayaChemTools; if not, see <http://www.gnu.org/licenses/> or
# write to the Free Software Foundation Inc., 59 Temple Place, Suite 330,
# Boston, MA, 02111-1307, USA.
#

"""
RDKitDrawMolecules.py - Draw molecules and generate an image file

Usage:
    RDKitDrawMolecules.py [--alignmentSMARTS <SMARTS>] [--atomLabelFontSize <number>]
                             [--bondLineWidth <number>] [--compute2DCoords <yes | no>] [--fontBold <yes or no>]
                             [--highlightSMARTS <SMARTS>] [--infileParams <Name,Value,...>] [--kekulize <yes or no>]
                             [--molImageSize <width,height>] [--numOfMolsPerRow <number>] [--overwrite]
                             [--showMolName <yes or no>] [-w <dir>] -i <infile> -o <outfile>
    RDKitDrawMolecules.py -h | --help | -e | --examples

Description:
    Draw molecules in a grid and write them out as an image file. The SVG image file
    appears to be the best among all the available image file options, as rendered in a
    browser. The Python modules aggdraw/cairo are required to generate high quality
    PNG images.

    The options '--atomLabelFontSize' and '--bondLineWidth' don't appear
    to work during generation of a SVG image.

    The supported input file formats are: Mol (.mol), SD (.sdf, .sd), SMILES (.smi,
    .txt, .csv, .tsv)

    The output image file can be saved in any format supported by the Python Image
    Library (PIL). The image format is automatically detected from the output file extension.

    Some of the most common output image file formats are: GIF (.gif), JPEG (.jpg),
    PNG (.png), SVG (.svg), TIFF (.tif)

Options:
    --alignmentSMARTS <SMARTS>  [default: none]
        SMARTS pattern for aligning molecules to a common template.
    --atomLabelFontSize <number>  [default: 12]
        Font size for drawing atom labels. This option is ignored during generation of a SVG
        output file.
    -b, --bondLineWidth <number>  [default: 1.2]
        Line width for drawing bonds. This option is ignored during generation of a SVG
        output file.
    -c, --compute2DCoords <yes | no>  [default: auto]
        Compute 2D coordinates of molecules before drawing. Default: yes for SMILES
        file; no for all other file types.
    -e, --examples
        Print examples.
    -f --fontBold <yes or no>  [default: yes]
        Make all text fonts bold during generation of  a SVG output file. This option is ignored for
        all other output files.
    -h, --help
        Print this help message.
    --highlightSMARTS <SMARTS>  [default: none]
        SMARTS pattern for highlighting atoms and bonds in molecules. All matched
        substructures are highlighted.
    -i, --infile <infile>
        Input file name.
    --infileParams <Name,Value,...>  [default: auto]
        A comma delimited list of parameter name and value pairs for reading
        molecules from files. The supported parameter names for different file
        formats, along with their default values, are shown below:
            
            SD, MOL: removeHydrogens,yes,sanitize,yes,strictParsing,yes
            SMILES: smilesColumn,1,smilesNameColumn,2,smilesDelimiter,space,
                smilesTitleLine,auto,sanitize,yes
            
        Possible values for smilesDelimiter: space, comma or tab.
    -k, --kekulize <yes or no>  [default: yes]
        Perform kekulization on molecules. This option is ignored during generation of a SVG
        output file.
    -m, --molImageSize <width,height>  [default: 400,300]
        Image size of a molecule in pixels.
    -n, --numOfMolsPerRow <number>  [default: 2]
        Number of molecules to draw in a row.
    -o, --outfile <outfile>
        Output file name.
    --overwrite
        Overwrite existing files.
    -s, --showMolName <yes or no>  [default: yes]
        Show molecule names under the images.
    -w, --workingdir <dir>
        Location of working directory which defaults to the current directory.

Examples:
    To automatically compute 2D coordinates for molecules in a SMILES file and
    generate a SVG image file containing 2 molecules per row in a grid with cell
    size of 400 x 300 pixels, type:

        % RDKitDrawMolecules.py -i Sample.smi -o SampleOut.svg

    To automatically compute 2D coordinates for molecules in a SMILES file and
    generate a SVG image file containing 4 molecules per row in a grid with cell
    size of 200 x 200 pixels and without any keulization along with highlighting
    a specific set of atoms and bonds indicated by a SMARTS pattern, type:

        % RDKitDrawMolecules.py -n 4 -m "200,200" -k no --fontBold no
          --highlightSMARTS  'c1ccccc1' -i Sample.smi -o SampleOut.svg

    To generate a PNG image file for molecules in a SD file using existing 2D
    coordinates, type

        % RDKitDrawMolecules.py --compute2DCoords no -i Sample.sdf
          -o SampleOut.png

    To automatically compute 2D coordinates for molecules in a CSV SMILES file
    with column headers, SMILES strings in column 1, and name in column 2 and
    generate a PDF image file, type:

        % RDKitDrawMolecules.py --infileParams "smilesDelimiter,comma,
          smilesTitleLine,yes,smilesColumn,1,smilesNameColumn,2"
          -i SampleSMILES.csv -o SampleOut.pdf

Author:
    Manish Sud(msud@san.rr.com)

See also:
    RDKitConvertFileFormat.py, RDKitRemoveDuplicateMolecules.py, RDKitSearchFunctionalGroups.py,
    RDKitSearchSMARTS.py

Copyright:
    Copyright (C) 2018 Manish Sud. All rights reserved.

    The functionality available in this script is implemented using RDKit, an
    open source toolkit for cheminformatics developed by Greg Landrum.

    This file is part of MayaChemTools.

    MayaChemTools is free software; you can redistribute it and/or modify it under
    the terms of the GNU Lesser General Public License as published by the Free
    Software Foundation; either version 3 of the License, or (at your option) any
    later version.

"""

from __future__ import print_function

# Add local python path to the global path and import appropriate modules...
import os
import sys;  sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), "..", "lib", "Python"))
import time
import re

# RDKit imports...
try:
    from rdkit import rdBase
    from rdkit import Chem
    from rdkit.Chem import AllChem
    from rdkit.Chem import Draw
    from rdkit.Chem.Draw.MolDrawing import DrawingOptions
except ImportError as ErrMsg:
    sys.stderr.write("\nFailed to import RDKit module/package: %s\n" % ErrMsg)
    sys.stderr.write("Check/update your RDKit environment and try again.\n\n")
    sys.exit(1)

# MayaChemTools imports...
try:
    from docopt import docopt
    import MiscUtil
    import RDKitUtil
except ImportError as ErrMsg:
    sys.stderr.write("\nFailed to import MayaChemTools module/package: %s\n" % ErrMsg)
    sys.stderr.write("Check/update your MayaChemTools environment and try again.\n\n")
    sys.exit(1)

ScriptName = os.path.basename(sys.argv[0])
Options = {}
OptionsInfo = {}

def main():
    """Start execution of the script"""
    
    MiscUtil.PrintInfo("\n%s (RDK v%s): Starting...\n" % (ScriptName, rdBase.rdkitVersion))
    
    (WallClockTime, ProcessorTime) = MiscUtil.GetWallClockAndProcessorTime()
    
    # Retrieve command line arguments and options...
    RetrieveOptions()
    
    # Process and validate command line arguments and options...
    ProcessOptions()
    
    # Perform actions required by the script...
    DrawMolecules()
    
    MiscUtil.PrintInfo("\n%s: Done...\n" % ScriptName)
    MiscUtil.PrintInfo("Total time: %s" % MiscUtil.GetFormattedElapsedTime(WallClockTime, ProcessorTime))

def DrawMolecules():
    """Draw molecules"""
    
    Infile = OptionsInfo["Infile"]
    Outfile = OptionsInfo["Outfile"]
    
    # Read molecules...
    MiscUtil.PrintInfo("\nReading file %s..." % Infile)

    ValidMols, MolCount, ValidMolCount  = RDKitUtil.ReadAndValidateMolecules(Infile, **OptionsInfo["InfileParams"])
    
    MiscUtil.PrintInfo("Total number of molecules: %d" % MolCount)
    MiscUtil.PrintInfo("Number of valid molecules: %d" % ValidMolCount)
    MiscUtil.PrintInfo("Number of ignored molecules: %d" % (MolCount - ValidMolCount))

    # Compute 2D coordinates...
    if OptionsInfo["Compute2DCoords"]:
        MiscUtil.PrintInfo("\nComputing 2D coordinates...")
        for Mol in ValidMols:
            AllChem.Compute2DCoords(Mol)
    
    MiscUtil.PrintInfo("Generating image grid...")
    
    # Setup atoms lists for highlighting atoms and bonds...
    AtomListsToHighlight = SetupAtomListsToHighlight(ValidMols)
    BondListsToHighlight = None
        
    # Set up legends...
    MolNames = None
    if OptionsInfo["ShowMolName"]:
        MolNames = []
        MolCount = 0
        for Mol in ValidMols:
            MolCount += 1
            MolName = RDKitUtil.GetMolName(Mol, MolCount)
            MolNames.append(MolName)
    
    # Perform alignment to a common template...
    PerformAlignment(ValidMols)
    
    # Generate molecule images...
    NumOfMolsPerRow = OptionsInfo["NumOfMolsPerRow"]
    Width = OptionsInfo["MolImageWidth"]
    Height = OptionsInfo["MolImageHeight"]

    # Setup drawing options...
    UpdatedDrawingOptions = DrawingOptions()
    UpdatedDrawingOptions.atomLabelFontSize = int(OptionsInfo["AtomLabelFontSize"])
    UpdatedDrawingOptions.bondLineWidth = float(OptionsInfo["BondLineWidth"])
    
    # Setup generation of SVG image...
    UseSVG= False
    if MiscUtil.CheckFileExt(Outfile, "svg"):
        UseSVG = True

    if UseSVG:
        MolsImage = Draw.MolsToGridImage(ValidMols, molsPerRow = NumOfMolsPerRow, subImgSize = (Width,Height), legends = MolNames, highlightAtomLists = AtomListsToHighlight, highlightBondLists = BondListsToHighlight, useSVG = UseSVG)

        # It appears that the string 'xmlns:svg' needs to be replaced with 'xmlns' in the
        # SVG image string generated by RDKit. Otherwise, the image doesn't load in 
        # web browsers.
        #
        if re.search("xmlns:svg", MolsImage, re.I):
            MolsImage = re.sub("xmlns:svg", "xmlns", MolsImage)
        
        # Make mol names bold...
        if OptionsInfo["FontBold"]:
            MolsImage = re.sub("font-weight:normal;", "font-weight:bold;", MolsImage)
        
    else:
        MolsImage = Draw.MolsToGridImage(ValidMols, molsPerRow = NumOfMolsPerRow,  subImgSize = (Width,Height), legends = MolNames, highlightAtomLists = AtomListsToHighlight, highlightBondLists = BondListsToHighlight, useSVG = UseSVG, kekulize = OptionsInfo["Kekulize"],  options = UpdatedDrawingOptions)

    # Write out the image file...
    MiscUtil.PrintInfo("\nGenerating image file %s..." % Outfile)
    
    if UseSVG:
        OutFH = open(Outfile, "w")
        OutFH.write(MolsImage)
        OutFH.close()
    else:
        if MiscUtil.CheckFileExt(Outfile, "pdf"):
            if MolsImage.mode == 'RGBA':
                MolsImage = MolsImage.convert('RGB')

        MolsImage.save(Outfile)

def SetupAtomListsToHighlight(ValidMols):
    """Set up atom lists to highlight using specified SMARTS pattern."""

    AtomListsToHighlight = None
    if OptionsInfo["HighlightSMARTSPattern"] is None:
        return  AtomListsToHighlight
    
    PatternMol = Chem.MolFromSmarts(OptionsInfo["HighlightSMARTSPattern"])
    AtomListsToHighlight = []
    for ValidMol in ValidMols:
        # Get matched atom lists and flatten it...
        MatchedAtomsLists = ValidMol.GetSubstructMatches(PatternMol)
        MatchedAtoms = [ Atom for AtomsList in MatchedAtomsLists for Atom in AtomsList] 
        AtomListsToHighlight.append(MatchedAtoms)
    
    return  AtomListsToHighlight

def PerformAlignment(ValidMols):
    """Perform alignment to a common template specified by a SMARTS pattern."""
    
    if OptionsInfo["AlignmentSMARTSPattern"] is None:
        return
    
    PatternMol = Chem.MolFromSmarts(OptionsInfo["AlignmentSMARTSPattern"])
    AllChem.Compute2DCoords(PatternMol)
        
    MatchedValidMols = [ValidMol for ValidMol in ValidMols if ValidMol.HasSubstructMatch(PatternMol)]
    for ValidMol in MatchedValidMols:
        AllChem.GenerateDepictionMatching2DStructure(ValidMol, PatternMol)

def ProcessOptions():
    """Process and validate command line arguments and options"""
    
    MiscUtil.PrintInfo("Processing options...")
    
    # Validate options...
    ValidateOptions()
    
    OptionsInfo["Infile"] = Options["--infile"]
    OptionsInfo["Outfile"] = Options["--outfile"]
    OptionsInfo["Overwrite"] = Options["--overwrite"]
    
    # No need for any RDKit specific --outfileParams....
    OptionsInfo["InfileParams"] = MiscUtil.ProcessOptionInfileParameters("--infileParams", Options["--infileParams"], OptionsInfo["Infile"])

    AlignmentSMARTSPattern = None
    if not re.match("^None$", Options["--alignmentSMARTS"], re.I):
        AlignmentSMARTSPattern = Options["--alignmentSMARTS"]
    OptionsInfo["AlignmentSMARTSPattern"]  = AlignmentSMARTSPattern
    
    OptionsInfo["AtomLabelFontSize"] = Options["--atomLabelFontSize"]
    OptionsInfo["BondLineWidth"] = Options["--bondLineWidth"]
    
    Compute2DCoords = False
    if re.match("^yes$", Options["--compute2DCoords"], re.I):
        Compute2DCoords = True
    elif re.match("^no$", Options["--compute2DCoords"], re.I):
        Compute2DCoords = False
    else:
        if MiscUtil.CheckFileExt(OptionsInfo["Infile"] ,"smi"):
            Compute2DCoords = True
    OptionsInfo["Compute2DCoords"]  = Compute2DCoords

    OptionsInfo["FontBold"] = True
    if re.match("^no$", Options["--fontBold"], re.I):
        OptionsInfo["FontBold"] = False
        
    HighlightSMARTSPattern = None
    if not re.match("^None$", Options["--highlightSMARTS"], re.I):
        HighlightSMARTSPattern = Options["--highlightSMARTS"]
    OptionsInfo["HighlightSMARTSPattern"]  = HighlightSMARTSPattern
    
    OptionsInfo["Kekulize"] = True
    if re.match("^no$", Options["--kekulize"], re.I):
        OptionsInfo["Kekulize"] = False
        
    SizeValues = Options["--molImageSize"].split(",")
    OptionsInfo["MolImageWidth"] = int(SizeValues[0])
    OptionsInfo["MolImageHeight"] = int(SizeValues[1])

    OptionsInfo["NumOfMolsPerRow"] = int(Options["--numOfMolsPerRow"])

    OptionsInfo["ShowMolName"] = True
    if re.match("^no$", Options["--showMolName"], re.I):
        OptionsInfo["ShowMolName"] = False

def RetrieveOptions():
    """Retrieve command line arguments and options"""
    
    # Get options...
    global Options
    Options = docopt(__doc__)
    
    # Set current working directory to the specified directory...
    WorkingDir = Options["--workingdir"]
    if WorkingDir:
        os.chdir(WorkingDir)
    
    # Handle examples option...
    if "--examples" in Options and Options["--examples"]:
        MiscUtil.PrintInfo(MiscUtil.GetExamplesTextFromDocOptText(__doc__))
        sys.exit(0)

def ValidateOptions():
    """Validate option values"""
    
    MiscUtil.ValidateOptionFilePath("-i, --infile", Options["--infile"])
    MiscUtil.ValidateOptionFileExt("-i, --infile", Options["--infile"], "sdf sd mol smi csv tsv txt")

    MiscUtil.ValidateOptionsOutputFileOverwrite("-o, --outfile", Options["--outfile"], "--overwrite", Options["--overwrite"])
    MiscUtil.ValidateOptionsDistinctFileNames("-i, --infile", Options["--infile"], "-o, --outfile", Options["--outfile"])
    
    if not re.match("^None$", Options["--alignmentSMARTS"], re.I):
        PatternMol = Chem.MolFromSmarts(Options["--alignmentSMARTS"])
        if PatternMol is None:
            MiscUtil.PrintError("The value specified, %s, using option \"--alignmentSMARTS\" is not a valid SMARTS: Failed to create pattern molecule" % Options["--alignmentSMARTS"])
    
    MiscUtil.ValidateOptionNumberValue("--atomLabelFontSize", int(Options["--atomLabelFontSize"]), {">": 0})
    MiscUtil.ValidateOptionNumberValue("-b, --bondLineWidth", float(Options["--bondLineWidth"]), {">": 0.0})
    
    MiscUtil.ValidateOptionTextValue("--compute2DCoords", Options["--compute2DCoords"], "yes no auto")
    
    MiscUtil.ValidateOptionTextValue("--f, -fontBold", Options["--fontBold"], "yes no")
    
    if not re.match("^None$", Options["--highlightSMARTS"], re.I):
        PatternMol = Chem.MolFromSmarts(Options["--highlightSMARTS"])
        if PatternMol is None:
            MiscUtil.PrintError("The value specified, %s, using option \"--highlightSMARTS\" is not a valid SMARTS: Failed to create pattern molecule" % Options["--highlightSMARTS"])
    
    MiscUtil.ValidateOptionTextValue("--kekulize", Options["--kekulize"], "yes no")
    
    MiscUtil.ValidateOptionNumberValues("-m, --molImageSize", Options["--molImageSize"], 2, ",", "integer", {">": 0})
    MiscUtil.ValidateOptionNumberValue("--numOfMolsPerRow", int(Options["--numOfMolsPerRow"]), {">": 0})
    
    MiscUtil.ValidateOptionTextValue("--showMolName", Options["--showMolName"], "yes no")

if __name__ == "__main__":
    main()
