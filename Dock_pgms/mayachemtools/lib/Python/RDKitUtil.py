#
# File: RDKitUtil.py
# Author: Manish Sud <msud@san.rr.com>
#
# Copyright (C) 2018 Manish Sud. All rights reserved.
#
# The functionality available in the script is implemented using RDKit, an
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

from __future__ import print_function

import os
import sys
import re

from rdkit import Chem
from rdkit.Chem import AllChem

import MiscUtil

__all__ = ["GetMolName", "IsMolEmpty", "ReadMolecules", "ReadAndValidateMolecules", "ReadMoleculesFromSDFile", "ReadMoleculesFromMolFile", "ReadMoleculesFromMol2File", "ReadMoleculesFromPDBFile", "ReadMoleculesFromSMILESFile", "WriteMolecules"]

def GetMolName(Mol, MolNum = None):
    """Get molecule name.
    
    Arguments:
        Mol (object): RDKit molecule object.
        MolNum (int or None): Molecule number in input file.

    Returns:
        str : Molname corresponding to _Name property of a molecule, generated
            from specieid MolNum using the format "Mol%d" % MolNum, or an
            empty string.

    """
    
    MolName = ''
    if Mol.HasProp("_Name"):
        MolName = Mol.GetProp("_Name")

    if not len(MolName):
        if MolNum is not None:
            MolName = "Mol%d" % MolNum
    
    return MolName

def IsMolEmpty(Mol):
    """Check for the presence of atoms in a molecule.
    
    Arguments:
        Mol (object): RDKit molecule object.

    Returns:
        bool : True - No atoms in molecule; Otherwise, false. 

    """

    Status = False if Mol.GetNumAtoms() else True
    
    return Status

def ReadAndValidateMolecules(FileName, **KeyWordArgs):
    """Read molecules from an input file, validate all molecule objects, and return
    a list of valid and non-valid molecule objects along with their counts.
    
    Arguments:
        FileName (str): Name of a file with complete path.
        **KeyWordArgs (dictionary) : Parameter name and value pairs for reading and
            processing molecules.

    Returns:
        list : List of valid RDKit molecule objects.
        int : Number of total molecules in input file. 
        int : Number of valid molecules in input file. 

    Notes:
        The file extension is used to determine type of the file and set up an appropriate
        file reader.

    """

    AllowEmptyMols = True
    if "AllowEmptyMols" in KeyWordArgs:
        AllowEmptyMols = KeyWordArgs["AllowEmptyMols"]
    
    Mols = ReadMolecules(FileName, **KeyWordArgs)

    if AllowEmptyMols:
        ValidMols = [Mol for Mol in Mols if Mol is not None]
    else:
        ValidMols = []
        MolCount = 0
        for Mol in Mols:
            MolCount += 1
            if Mol is None:
                continue
            
            if IsMolEmpty(Mol):
                MolName = GetMolName(Mol, MolCount)
                MiscUtil.PrintWarning("Ignoring empty molecule: %s" % MolName)
                continue
            
            ValidMols.append(Mol)
            
    MolCount = len(Mols)
    ValidMolCount = len(ValidMols)

    return (ValidMols, MolCount, ValidMolCount)

def ReadMolecules(FileName, **KeyWordArgs):
    """Read molecules from an input file without performing any validation
    and creation of molecule objects.
    
    Arguments:
        FileName (str): Name of a file with complete path.
        **KeyWordArgs (dictionary) : Parameter name and value pairs for reading and
            processing molecules.

    Returns:
        list : List of RDKit molecule objects.

    Notes:
        The file extension is used to determine type of the file and set up an appropriate
        file reader.

    """

    # Set default values for possible arguments...
    ReaderArgs = {"Sanitize": True, "RemoveHydrogens": True, "StrictParsing": True,  "SMILESDelimiter" : ' ', "SMILESColumn": 1, "SMILESNameColumn": 2, "SMILESTitleLine": True }

    # Set specified values for possible arguments...
    for Arg in ReaderArgs:
        if Arg in KeyWordArgs:
            ReaderArgs[Arg] = KeyWordArgs[Arg]

    # Modify specific valeus for SMILES...
    if MiscUtil.CheckFileExt(FileName, "smi csv tsv txt"):
        Args = ["Sanitize", "SMILESTitleLine"]
        for Arg in Args:
            if ReaderArgs[Arg] is True:
                ReaderArgs[Arg] = 1
            else:
                ReaderArgs[Arg] = 0
    
    Mols = []
    if MiscUtil.CheckFileExt(FileName, "sdf sd"):
        return ReadMoleculesFromSDFile(FileName, ReaderArgs["Sanitize"], ReaderArgs["RemoveHydrogens"], ReaderArgs['StrictParsing'])
    elif MiscUtil.CheckFileExt(FileName, "mol"):
        return ReadMoleculesFromMolFile(FileName, ReaderArgs["Sanitize"], ReaderArgs["RemoveHydrogens"], ReaderArgs['StrictParsing'])
    elif MiscUtil.CheckFileExt(FileName, "mol2"):
        return ReadMoleculesFromMol2File(FileName, ReaderArgs["Sanitize"], ReaderArgs["RemoveHydrogens"])
    elif MiscUtil.CheckFileExt(FileName, "pdb"):
        return ReadMoleculesFromPDBFile(FileName, ReaderArgs["Sanitize"], ReaderArgs["RemoveHydrogens"])
    elif MiscUtil.CheckFileExt(FileName, "smi txt csv tsv"):
        SMILESColumnIndex = ReaderArgs["SMILESColumn"] - 1
        SMILESNameColumnIndex = ReaderArgs["SMILESNameColumn"] - 1
        return ReadMoleculesFromSMILESFile(FileName, ReaderArgs["SMILESDelimiter"], SMILESColumnIndex, SMILESNameColumnIndex, ReaderArgs["SMILESTitleLine"], ReaderArgs["Sanitize"])
    else:
        MiscUtil.PrintWarning("RDKitUtil.ReadMolecules: Non supported file type: %s" % FileName)
    
    return Mols

def ReadMoleculesFromSDFile(FileName, Sanitize = True, RemoveHydrogens = True, StrictParsing = True):
    """Read molecules from a SD file.
    
    Arguments:
        FileName (str): Name of a file with complete path.
        Sanitize (bool): Sanitize molecules.
        RemoveHydrogens (bool): Remove hydrogens from molecules.
        StrictParsing (bool): Perform strict parsing.

    Returns:
        list : List of RDKit molecule objects.

    """
    return  Chem.SDMolSupplier(FileName, sanitize = Sanitize, removeHs = RemoveHydrogens, strictParsing = StrictParsing)

def ReadMoleculesFromMolFile(FileName, Sanitize = True, RemoveHydrogens = True, StrictParsing = True):
    """Read molecule from a MDL Mol file.
    
    Arguments:
        FileName (str): Name of a file with complete path.
        Sanitize (bool): Sanitize molecules.
        RemoveHydrogens (bool): Remove hydrogens from molecules.
        StrictParsing (bool): Perform strict parsing.

    Returns:
        list : List of RDKit molecule objects.

    """
    
    Mols = []
    Mols.append(Chem.MolFromMolFile(FileName, sanitize = Sanitize, removeHs = RemoveHydrogens, strictParsing = StrictParsing))
    return Mols

def ReadMoleculesFromMol2File(FileName, Sanitize = True, RemoveHydrogens = True):
    """Read molecule from a Tripos Mol2  file.
    
    Arguments:
        FileName (str): Name of a file with complete path.
        Sanitize (bool): Sanitize molecules.
        RemoveHydrogens (bool): Remove hydrogens from molecules.

    Returns:
        list : List of RDKit molecule objects.

    """
    
    Mols = []
    Mols.append(Chem.MolFromMol2File(FileName,  sanitize = Sanitize, removeHs = RemoveHydrogens))
    return Mols

def ReadMoleculesFromPDBFile(FileName, Sanitize = True, RemoveHydrogens = True):
    """Read molecule from a PDB  file.
    
    Arguments:
        FileName (str): Name of a file with complete path.
        Sanitize (bool): Sanitize molecules.
        RemoveHydrogens (bool): Remove hydrogens from molecules.

    Returns:
        list : List of RDKit molecule objects.

    """
    
    Mols = []
    Mols.append(Chem.MolFromPDBFile(FileName,  sanitize = Sanitize, removeHs = RemoveHydrogens))
    return Mols

def ReadMoleculesFromSMILESFile(FileName, SMILESDelimiter = ' ', SMILESColIndex = 0, SMILESNameColIndex = 1, SMILESTitleLine = 1, Sanitize = 1):
    """Read molecules from a SMILES file.
    
    Arguments:
        SMILESDelimiter (str): Delimiter for parsing SMILES line
        SMILESColIndex (int): Column index containing SMILES string.
        SMILESNameColIndex (int): Column index containing molecule name.
        SMILESTitleLine (int): Flag to indicate presence of title line.
        Sanitize (int): Sanitize molecules.

    Returns:
        list : List of RDKit molecule objects.

    """
    
    return  Chem.SmilesMolSupplier(FileName, delimiter = SMILESDelimiter, smilesColumn = SMILESColIndex, nameColumn = SMILESNameColIndex, titleLine = SMILESTitleLine, sanitize = Sanitize)

def MoleculesWriter(FileName, **KeyWordArgs):
    """Set up a molecule writer.
    
    Arguments:
        FileName (str): Name of a file with complete path.
        **KeyWordArgs (dictionary) : Parameter name and value pairs for writing and
            processing molecules.

    Returns:
        RDKit object : Molecule writer.

    Notes:
        The file extension is used to determine type of the file and set up an appropriate
        file writer.

    """
    
    # Set default values for possible arguments...
    WriterArgs = {"Compute2DCoords" : False, "Kekulize": False, "SMILESDelimiter" : ' ', "SMILESIsomeric": True, "SMILESTitleLine": True }

    # Set specified values for possible arguments...
    for Arg in WriterArgs:
        if Arg in KeyWordArgs:
            WriterArgs[Arg] = KeyWordArgs[Arg]
    
    Writer = None
    if MiscUtil.CheckFileExt(FileName, "sdf sd"):
        Writer = Chem.SDWriter(FileName)
        if WriterArgs["Kekulize"]:
            Writer.SetKekulize(True)
    elif MiscUtil.CheckFileExt(FileName, "pdb"):
        Writer = Chem.PDBWriter(FileName)
    elif MiscUtil.CheckFileExt(FileName, "smi"):
        # Text for the name column in the title line. Blank indicates not to include name column
        # in the output file...
        NameHeader = 'Name'
        Writer = Chem.SmilesWriter(FileName, delimiter = WriterArgs["SMILESDelimiter"], nameHeader = NameHeader, includeHeader = WriterArgs["SMILESTitleLine"],  isomericSmiles = WriterArgs["SMILESIsomeric"], kekuleSmiles = WriterArgs["Kekulize"])
    else:
        MiscUtil.PrintWarning("RDKitUtil.WriteMolecules: Non supported file type: %s" % FileName)
    
    return Writer
    
def WriteMolecules(FileName, Mols, **KeyWordArgs):
    """Write molecules to an output file.
    
    Arguments:
        FileName (str): Name of a file with complete path.
        Mols (list): List of RDKit molecule objects. 
        **KeyWordArgs (dictionary) : Parameter name and value pairs for writing and
            processing molecules.

    Returns:
        int : Number of total molecules.
        int : Number of processed molecules written to output file.

    Notes:
        The file extension is used to determine type of the file and set up an appropriate
        file writer.

    """
    
    Compute2DCoords = False
    if "Compute2DCoords" in KeyWordArgs:
        Compute2DCoords = KeyWordArgs["Compute2DCoords"]
        
    MolCount = len(Mols)
    ProcessedMolCount = 0
    
    Writer = MoleculesWriter(FileName, **KeyWordArgs)
    
    if Writer is None:
        return (MolCount, ProcessedMolCount)
    
    for Mol in Mols:
        if Mol is None:
            continue
        
        ProcessedMolCount += 1
        if Compute2DCoords:
            AllChem.Compute2DCoords(Mol)
        
        Writer.write(Mol)
    
    Writer.close()
    
    return (MolCount, ProcessedMolCount)
