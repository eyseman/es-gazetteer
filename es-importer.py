import csv
import time
import multiprocessing

from elasticsearch import Elasticsearch, helpers
from tqdm import tqdm
from datetime import datetime

es = Elasticsearch(urls='http://localhost:9200/', timeout=60, max_retries=2)
number_of_threads = multiprocessing.cpu_count()


def iso_convert(iso2c):
    """
    Takes a two character ISO country code and returns the corresponding 3
    character ISO country code.
    Parameters
    ----------
    iso2c: A two character ISO country code.
    Returns
    -------
    iso3c: A three character ISO country code.
    """

    iso_dict = {"AD": "AND", "AE": "ARE", "AF": "AFG", "AG": "ATG", "AI": "AIA",
                "AL": "ALB", "AM": "ARM", "AO": "AGO", "AQ": "ATA", "AR": "ARG",
                "AS": "ASM", "AT": "AUT", "AU": "AUS", "AW": "ABW", "AX": "ALA",
                "AZ": "AZE", "BA": "BIH", "BB": "BRB", "BD": "BGD", "BE": "BEL",
                "BF": "BFA", "BG": "BGR", "BH": "BHR", "BI": "BDI", "BJ": "BEN",
                "BL": "BLM", "BM": "BMU", "BN": "BRN", "BO": "BOL", "BQ": "BES",
                "BR": "BRA", "BS": "BHS", "BT": "BTN", "BV": "BVT", "BW": "BWA",
                "BY": "BLR", "BZ": "BLZ", "CA": "CAN", "CC": "CCK", "CD": "COD",
                "CF": "CAF", "CG": "COG", "CH": "CHE", "CI": "CIV", "CK": "COK",
                "CL": "CHL", "CM": "CMR", "CN": "CHN", "CO": "COL", "CR": "CRI",
                "CU": "CUB", "CV": "CPV", "CW": "CUW", "CX": "CXR", "CY": "CYP",
                "CZ": "CZE", "DE": "DEU", "DJ": "DJI", "DK": "DNK", "DM": "DMA",
                "DO": "DOM", "DZ": "DZA", "EC": "ECU", "EE": "EST", "EG": "EGY",
                "EH": "ESH", "ER": "ERI", "ES": "ESP", "ET": "ETH", "FI": "FIN",
                "FJ": "FJI", "FK": "FLK", "FM": "FSM", "FO": "FRO", "FR": "FRA",
                "GA": "GAB", "GB": "GBR", "GD": "GRD", "GE": "GEO", "GF": "GUF",
                "GG": "GGY", "GH": "GHA", "GI": "GIB", "GL": "GRL", "GM": "GMB",
                "GN": "GIN", "GP": "GLP", "GQ": "GNQ", "GR": "GRC", "GS": "SGS",
                "GT": "GTM", "GU": "GUM", "GW": "GNB", "GY": "GUY", "HK": "HKG",
                "HM": "HMD", "HN": "HND", "HR": "HRV", "HT": "HTI", "HU": "HUN",
                "ID": "IDN", "IE": "IRL", "IL": "ISR", "IM": "IMN", "IN": "IND",
                "IO": "IOT", "IQ": "IRQ", "IR": "IRN", "IS": "ISL", "IT": "ITA",
                "JE": "JEY", "JM": "JAM", "JO": "JOR", "JP": "JPN", "KE": "KEN",
                "KG": "KGZ", "KH": "KHM", "KI": "KIR", "KM": "COM", "KN": "KNA",
                "KP": "PRK", "KR": "KOR", "XK": "XKX", "KW": "KWT", "KY": "CYM",
                "KZ": "KAZ", "LA": "LAO", "LB": "LBN", "LC": "LCA", "LI": "LIE",
                "LK": "LKA", "LR": "LBR", "LS": "LSO", "LT": "LTU", "LU": "LUX",
                "LV": "LVA", "LY": "LBY", "MA": "MAR", "MC": "MCO", "MD": "MDA",
                "ME": "MNE", "MF": "MAF", "MG": "MDG", "MH": "MHL", "MK": "MKD",
                "ML": "MLI", "MM": "MMR", "MN": "MNG", "MO": "MAC", "MP": "MNP",
                "MQ": "MTQ", "MR": "MRT", "MS": "MSR", "MT": "MLT", "MU": "MUS",
                "MV": "MDV", "MW": "MWI", "MX": "MEX", "MY": "MYS", "MZ": "MOZ",
                "NA": "NAM", "NC": "NCL", "NE": "NER", "NF": "NFK", "NG": "NGA",
                "NI": "NIC", "NL": "NLD", "NO": "NOR", "NP": "NPL", "NR": "NRU",
                "NU": "NIU", "NZ": "NZL", "OM": "OMN", "PA": "PAN", "PE": "PER",
                "PF": "PYF", "PG": "PNG", "PH": "PHL", "PK": "PAK", "PL": "POL",
                "PM": "SPM", "PN": "PCN", "PR": "PRI", "PS": "PSE", "PT": "PRT",
                "PW": "PLW", "PY": "PRY", "QA": "QAT", "RE": "REU", "RO": "ROU",
                "RS": "SRB", "RU": "RUS", "RW": "RWA", "SA": "SAU", "SB": "SLB",
                "SC": "SYC", "SD": "SDN", "SS": "SSD", "SE": "SWE", "SG": "SGP",
                "SH": "SHN", "SI": "SVN", "SJ": "SJM", "SK": "SVK", "SL": "SLE",
                "SM": "SMR", "SN": "SEN", "SO": "SOM", "SR": "SUR", "ST": "STP",
                "SV": "SLV", "SX": "SXM", "SY": "SYR", "SZ": "SWZ", "TC": "TCA",
                "TD": "TCD", "TF": "ATF", "TG": "TGO", "TH": "THA", "TJ": "TJK",
                "TK": "TKL", "TL": "TLS", "TM": "TKM", "TN": "TUN", "TO": "TON",
                "TR": "TUR", "TT": "TTO", "TV": "TUV", "TW": "TWN", "TZ": "TZA",
                "UA": "UKR", "UG": "UGA", "UM": "UMI", "US": "USA", "UY": "URY",
                "UZ": "UZB", "VA": "VAT", "VC": "VCT", "VE": "VEN", "VG": "VGB",
                "VI": "VIR", "VN": "VNM", "VU": "VUT", "WF": "WLF", "WS": "WSM",
                "YE": "YEM", "YT": "MYT", "ZA": "ZAF", "ZM": "ZMB", "ZW": "ZWE",
                "CS": "SCG", "AN": "ANT"}

    try:
        iso3c = iso_dict[iso2c]
        return iso3c
    except KeyError:
        print('Bad code: ' + iso2c)
        iso3c = "NA"
        return iso3c


def documents(reader, es):
    todays_date = datetime.today().strftime("%Y-%m-%d")
    count = 0
    for row in tqdm(reader, total=11741135):  # approx
        try:
            coords = row[4] + "," + row[5]
            country_code3 = iso_convert(row[8])
            doc = {"geonameid": row[0],
                   "name": row[1],
                   "asciiname": row[2],
                   "alternativenames": row[3].split(","),
                   "coordinates": coords,  # 4, 5
                   "feature_class": row[6],
                   "feature_code": row[7],
                   "country_code2": row[8],
                   "country_code3": country_code3,
                   "cc2": row[9],
                   "admin1_code": row[10],
                   "admin2_code": row[11],
                   "admin3_code": row[12],
                   "admin4_code": row[13],
                   "population": row[14],
                   "elevation": row[15],
                   "dem": row[16],
                   "timezone": row[17],
                   "modification_date": todays_date
                   }
            action = {"_index": "geonames",
                      "_type": "_doc",
                      "_id": doc['geonameid'],
                      "_source": doc}
            yield action
        except ():
            count += 1
    print('Exception count:', count)


if __name__ == "__main__":
    t = time.time()
    f = open('allCountries.txt', 'rt', encoding="utf8")
    reader = csv.reader(f, delimiter='\t')
    actions = documents(reader, es)
    for success, info in helpers.parallel_bulk(es, actions, chunk_size=500, thread_count=number_of_threads):
        if not success:
            print('A document failed:', info)
    es.indices.refresh(index='geonames')
    e = (time.time() - t) / 60
    print("Elapsed minutes: ", e)
