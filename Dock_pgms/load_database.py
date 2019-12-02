import gzip
import logging
from os import chdir, system, path, makedirs
from shutil import copyfileobj
from subprocess import check_output as run
from Dock_pgms import antechamber
from urllib2 import urlopen

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

# DATABASE = 'http://dud.docking.org/r2/dhfr.tar.gz'
DATABASE = '/databases.zip'
USERNAME = "james"
#DOWNLOADS = "/home/{}/Downloads".format(USERNAME)
DESKTOP = "/home/{}/Desktop/work/DHFR".format(USERNAME)
DOWNLOADS = DESKTOP + '/input_files'
DATABASE_FNAME = DATABASE.split("/")[-1]

data_fnames = ['dhfr_ligands', 'dhfr_decoys']
data_one = "{}/databases/dud_ligands2006/dhfr_ligands.sdf.gz".format(
    DOWNLOADS, DATABASE_FNAME)
data_second = "{}/databases/dud_decoys2006/dhfr_decoys.sdf.gz".format(
    DOWNLOADS, DATABASE_FNAME)

data_to_upload = [data_one,
                  data_second,
                  ]
FOLDERNAME = antechamber.FOLDER


def download_data():
    logging.info("Downloading database info{}".format(DOWNLOADS))
    chdir(DOWNLOADS)
    f = urlopen(DATABASE)
    with open(DATABASE_FNAME, "wb") as output:
        copyfileobj(f, output)

    logging.info("Extracting database".format(DOWNLOADS))
    run("tar -xvzf {}".format(DATABASE_FNAME), shell=True)
    upload_data()


def upload_data():
    logging.info("Moving DATA...")
    chdir(DESKTOP)
    for count, _data in enumerate(data_to_upload):
        # creation of folder1 and folder2
        folder = FOLDERNAME[count]
        if not path.exists(path.join(DESKTOP, folder)):
            makedirs(path.join(DESKTOP, folder))
        with gzip.open(_data, 'rb') as f_in, open(
                "{}/{}/{}.sdf".format(
                    DESKTOP, folder, data_fnames[count]), 'wb') as f_out:
            copyfileobj(f_in, f_out)
        logging.info("Moving DATA for {} completed!".format(folder))
        logging.info(
            "Starting babel script...Please wait a couple of minutes!")


if __name__ == "__main__":
    try:
        chdir('{}/databases'.format(DOWNLOADS))
        upload_data()
    except OSError:
        download_data()
