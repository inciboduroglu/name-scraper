import csv


class SpooderPipeline(object):

    def process_item(self, item, spider):
        # get category and use it as filename
        page_name = item["page_name"]
        filename = f'{page_name}.csv'
        del item["page_name"]

        with open(filename, 'a', newline='') as f:
            field_names = ['name', 'usage', 'gender', 'related-names']

            writer = csv.DictWriter(f, fieldnames=field_names)
            # writer.writeheader()
            writer.writerow(item)
