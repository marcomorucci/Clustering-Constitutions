import requests
from xlrd import open_workbook


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
