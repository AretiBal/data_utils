import wget
import os
import tarfile
import gzip
import shutil
import click

@click.command()
@click.option("--start", help="Start year", default=1960)
@click.option("--end", help="End year", default=2020)
@click.option("--output", help="Path to store the data", default=".")
def download_meteo_data(start=1960, end=2020, output="."):

    url = "https://zenodo.org/records/5947547/files/HySN2018v2005ERA5_historical_rsds_daily_{}.tar.gz"
    output_path = os.path.join(output, "HySN2018v2005ERA5_historical_rsds_daily_{}.tar.gz")

    if start < 1960:
        if end < 1960:
            print("No available data")
            return
        print("First available data in 1960")
        start = 1960

    start -= start %10

    if start < 2020:
        for decade in range(start, end, 10):

            output_filename = output_path.format(f"{decade}-{decade+9}")

            wget.download(url.format(f"{decade}-{decade+9}"), output_filename)

            with tarfile.open(output_filename, "r:gz") as tar:
                    tar.extractall(path=output)

            os.remove(output_filename)

    if start >= 2020 or end >= 2020:

        output_filename = output_path.format(2020).replace("tar", "nc4")

        wget.download(url.format(2020).replace(".tar",".nc4"), output_filename)

        # Unzip the .gz file , 2020 has a different format
        with gzip.open(output_filename, 'rb') as f_in:
            with open(output_filename.replace(".gz",""), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(output_filename)

if __name__ == "__main__":
    download_meteo_data()