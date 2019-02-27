import boto3
import json
import xlsxwriter

green = {"10 Gigabit", "20 Gigabit", "25 Gigabit", "50 Gigabit", "100 Gigabit"}
light_green = {"Up to 10 Gigabit", "Up to 25 Gigabit"}
yellow = {"Low to Moderate", "Moderate", "High", }
red = {"Low", "Very Low"}


def query_aws():
    client = boto3.client('pricing')

    paginator = client.get_paginator('get_products')

    response = paginator.paginate(
        ServiceCode='AmazonEC2',
        Filters=[
            {
                'Type': 'TERM_MATCH',
                'Field': 'tenancy',
                'Value': 'Shared'
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'operatingSystem',
                'Value': 'Linux'
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'tenancy',
                'Value': 'Shared'
            },
            {
                'Type': 'TERM_MATCH',
                'Field': 'preInstalledSw',
                'Value': "NA"
            }
        ],
    )

    res = dict()

    for page in response:
        for item in page["PriceList"]:
            item = json.loads(item)
            attr = item["product"]["attributes"]
            if "BoxUsage" in attr["usagetype"]:
                if attr["location"] not in res:
                    res[attr["location"]] = []
                else:
                    res[attr["location"]].append(item)

    return res


# with open('raw.json', 'w') as outfile:
#     json.dump(res, outfile, indent=2)
res = dict()
# with open('raw.json', 'r') as infile:
#     res = json.load(infile)
res = query_aws()

workbook = xlsxwriter.Workbook('instancesheet.xlsx')

bold = workbook.add_format({'bold': True})


def write_headers(worksheet):
    worksheet.write("A1", "Instance Type", bold)
    worksheet.write("B1", "VCPU", bold)
    worksheet.write("C1", "Memory", bold)
    worksheet.write("D1", "Network Performance", bold)


# def get_cost(terms):
#     for item in terms:

    # terms": {
    #         "OnDemand": {
    #             "2ZSKW5N6X86FEKAW.JRTCKXETXF": {
    #                 "priceDimensions": {
    #                     "2ZSKW5N6X86FEKAW.JRTCKXETXF.6YS6EN2CT7": {
    #                         "unit": "Hrs",
    #                         "endRange": "Inf",
    #                         "description": "$0.222 per On Demand Linux c5.xlarge Instance Hour",
    #                         "appliesTo": [],
    #                         "rateCode": "2ZSKW5N6X86FEKAW.JRTCKXETXF.6YS6EN2CT7",
    #                         "beginRange": "0",
    #                         "pricePerUnit": {
    #                             "USD": "0.2220000000"
    #                         }


for region, instances in res.items():
    worksheet = workbook.add_worksheet(region)
    write_headers(worksheet)
    worksheet.set_column('A:D', 18)
    worksheet.set_column('B:B', 6)
    for i, val in enumerate(instances):
        attr = val["product"]["attributes"]
        worksheet.write(i + 1, 0, attr["instanceType"])
        worksheet.write_number(i + 1, 1, int(attr["vcpu"]))
        worksheet.write(i + 1, 2, attr["memory"])
        cell_format = workbook.add_format()
        if attr["networkPerformance"] in green:
            cell_format.set_bg_color('green')
        elif attr["networkPerformance"] in light_green:
            cell_format.set_bg_color('#32CD32')
        elif attr["networkPerformance"] in red:
            cell_format.set_bg_color('red')
        elif attr["networkPerformance"] in yellow:
            cell_format.set_bg_color('yellow')
        else:
            cell_format.set_bg_color('white')

        worksheet.write(i + 1, 3, attr["networkPerformance"], cell_format)


workbook.close()
