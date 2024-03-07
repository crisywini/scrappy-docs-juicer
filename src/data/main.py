from docs_util import Scrappy
import pandas as pd

def main():
    scrappy = Scrappy('https://backstage.forgerock.com/docs/idcloud/latest/',
                      'https://backstage.forgerock.com/docs/idcloud/latest/overview.html')
    soups = scrappy.get_soups_from_base_path()
    dataframe = scrappy.get_content_as_dataframe(soups)
    dataframe.to_csv('scrappy-docs-juicer/data/raw/idcloud-content-script.csv')
    print(f'--Extracted all web sites available at {scrappy.base_path}-- ')
main()