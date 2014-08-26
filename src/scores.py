import requests
from xlrd import open_workbook
from pandas import read_csv


def load_workbook(path, index=0):
    wb = open_workbook(path)
    print "Loaded workbook with: ", wb.nsheets, 'sheets.'
    return wb.sheet_by_index(index)


def get_sfi_scores(path, col=4, names_path="../data/state_names.txt",
                   year=2010):
    with open(names_path, 'r+') as file:
        names = file.read().splitlines()

    sheet = loadWorkbook(path)

    scores = {}
    for r in range(1, sheet.nrows):
        if sheet.cell(r, 1).value in names and sheet.cell(r, 2).value == year:
            scores[sheet.cell(r, 1).value] = sheet.cell(r, col).value

    return scores


def get_fh_scores(sheet, countryCol=0, scoreCol=117, startRow=7):
    scores = {}
    for r in range(startRow, sheet.nrows):
        scores[sheet.cell(r, countryCol).value] = sheet.cell(r, scoreCol).value
    return scores


def clean_scores(scores, names_path):
    with open(names_path, 'r') as namesFile:
        names = namesFile.readlines()
    newScores = {}
    for n in names:
        n = n.rstrip('\n')
        newScores[n] = scores[n]

    return newScores


def create_score_slusters(clusters, scores):
    cScores = {}
    for c in clusters:
        cScores[c] = []
        for s in clusters[c]:
            cScores[c].append(scores[s])
    return cScores


def convert_scores(scores):
    for k in scores.keys():
        if scores[k] == "NF":
            scores[k] = 1
        elif scores[k] == "PF":
            scores[k] = 2
        elif scores[k] == "F":
            scores[k] = 3
    return scores


def clean_lji_scores(ind):
    ind = ind[ind['year'] == 2010]
    ind.loc[3353, 'country'] = "Bosnia-Herzegovina"
    ind.loc[5411, 'country'] = "Congo (Brazzaville)"
    ind.loc[5461, 'country'] = "Congo (Kinshasa)"
    ind.loc[9770, 'country'] = "Micronesia"
    ind.loc[4423, 'country'] = "Gambia, The"
    ind.loc[4740, 'country'] = "Cote d'Ivoire"
    ind.loc[4292, 'country'] = "Sao Tome & Principe"
    ind.loc[744, 'country'] = "Saint Kitts and Nevis"
    ind.loc[642, 'country'] = "Saint Lucia"
    ind.loc[678, 'country'] = "Saint Vincent & Grenadines"
    ind.loc[482, 'country'] = "Trinidad & Tobago"
    ind.loc[62, 'country'] = "United States"
    ind.loc[9030, 'country'] = "Vietnam, N."
    ind = ind.drop(9485)
    ind = ind.drop(3111)
    ind = ind.drop(2051)
    ind = ind.drop(3334)
    return ind


def get_gdp(sheet):
    gdp = {}
    for r in range(sheet.nrows):
        gdp[sheet.cell(r, 1).value] = sheet.cell(r, 2).value

    return gdp


def add_population(cdb, path="../data/population.csv"):
    pop = read_csv(path)
    pop['country_id'] = pop['Country Name']

    pop.loc[pop['Country Name'] == "Antigua and Barbuda", 'country_id'] = \
        "Antigua & Barbuda"
    pop.loc[pop['Country Name'] == "Bahamas, The", 'country_id'] = "Bahamas"
    pop.loc[pop['Country Name'] == "Bosnia and Herzegovina", 'country_id'] = \
        "Bosnia-Herzegovina"
    pop.loc[pop['Country Name'] == "Brunei Darussalam", 'country_id'] = \
        "Brunei"
    pop.loc[pop['Country Name'] == "Cabo Verde", 'country_id'] = "Cape Verde"
    pop.loc[pop['Country Name'] == "Congo, Dem. Rep.", 'country_id'] = \
        "Congo (Kinshasa)"
    pop.loc[pop['Country Name'] == "Congo, Rep.", 'country_id'] = \
        "Congo (Brazzaville)"
    pop.loc[pop['Country Name'] == "Egypt, Arab Rep.", 'country_id'] = "Egypt"
    pop.loc[pop['Country Name'] == "Iran, Islamic Rep.", 'country_id'] = "Iran"
    pop.loc[pop['Country Name'] == "Korea, Dem. Rep.", 'country_id'] = \
        "North Korea"
    pop.loc[pop['Country Name'] == "Korea, Rep.", 'country_id'] = "South Korea"
    pop.loc[pop['Country Name'] == "Kyrgyz Republic", 'country_id'] = \
        "Kyrgyzstan"
    pop.loc[pop['Country Name'] == "Lao PDR", 'country_id'] = "Laos"
    pop.loc[pop['Country Name'] == "Macedonia, FYR", 'country_id'] = \
        "Macedonia"
    pop.loc[pop['Country Name'] == "Micronesia, Fed. Sts.", 'country_id'] = \
        "Micronesia"
    pop.loc[pop['Country Name'] == "Myanmar", 'country_id'] = "Burma"
    pop.loc[pop['Country Name'] == "Russian Federation", 'country_id'] = \
        "Russia"
    pop.loc[pop['Country Name'] == "Sao Tome and Principe", 'country_id'] = \
        "Sao Tome & Principe"
    pop.loc[pop['Country Name'] == "Slovak Republic", 'country_id'] = \
        "Slovakia"
    pop.loc[pop['Country Name'] == "St. Kitts and Nevis", 'country_id'] = \
        "Saint Kitts and Nevis"
    pop.loc[pop['Country Name'] == "St. Lucia", 'country_id'] = "Saint Lucia"
    pop.loc[pop['Country Name'] == "St. Vincent and the Grenadines",
            'country_id'] = "Saint Vincent & Grenadines"
    pop.loc[pop['Country Name'] == "Syrian Arab Republic", 'country_id'] = \
        "Syria"
    pop.loc[pop['Country Name'] == "Timor-Leste", 'country_id'] = "East Timor"
    pop.loc[pop['Country Name'] == "Trinidad and Tobago", 'country_id'] = \
        "Trinidad & Tobago"
    pop.loc[pop['Country Name'] == "Venezuela, RB", 'country_id'] = "Venezuela"
    pop.loc[pop['Country Name'] == "Yemen, Rep.", 'country_id'] = "Yemen"

    for r in range(len(pop)):
        if pop.loc[r, 'country_id'] in [c for c in cdb['country']]:
            idx = cdb.loc[cdb['country'] == pop.loc[r, 'country_id'], :].index
            cdb.loc[idx, 'wb_country'] = pop.loc[r, 'Country Name']
            cdb.loc[idx, 'population'] = pop.loc[r, 'Population (Total)']

    # Manually impute these missing values
    cdb.loc[cdb['country'] == 'Nauru', 'wb_country'] = "Nauru"
    cdb.loc[cdb['country'] == 'Nauru', 'population'] = 9378
    cdb.loc[cdb['country'] == 'Taiwan', 'wb_country'] = "Taiwan"
    cdb.loc[cdb['country'] == 'Taiwan', 'population'] = 23162000


def add_region(cdb, path="../data/country_metadata.csv"):
    reg = read_csv(path, quotechar='"')

    for r in range(len(reg)):
        if reg.loc[r, 'Table Name'] in [c for c in cdb['wb_country']]:
            idx = cdb.loc[cdb['wb_country'] ==
                          reg.loc[r, 'Table Name'], :].index

            cdb.loc[idx, 'region'] = reg.loc[r, 'Region']
        else:
            print reg.loc[r, 'Table Name']

    cdb.loc[cdb['country'] == 'Nauru', 'region'] = "East Asia & Pacific"
    cdb.loc[cdb['country'] == 'Taiwan', 'region'] = "East Asia & Pacific"
    cdb.loc[cdb['country'] == "Cote d'Ivoire", "region"] = "Sub-Saharan Africa"
    cdb.loc[cdb['country'] == "Sao Tome & Principe", "region"] = \
        "Sub-Saharan Africa"
