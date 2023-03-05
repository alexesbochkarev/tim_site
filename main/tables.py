import datetime

import django_tables2 as tables

from main.models import Plugin, LegalUser, PhysicalUser


class PluginTable(tables.Table):
    class Meta:
        model = Plugin
        exclude = ("id", "user",)

    def create_table(self):
        main_html = """
<div class="table-container table-responsive">
<table class="table table-hover table-bordered align-middle">
    <thead>
    <tr>
    {0}
    </tr>
    </thead>
    <tbody>
    {1}
    </tbody>
</table>
</div>"""

        rows = [*self.data]
        if len(rows) == 0:
            return ""

        field_names = set(field.name for field in rows[0]._meta.get_fields()).difference(self.Meta.exclude)
        field_names = list(sorted(field_names, key=lambda x: rows[0].__dir__().index(x)))
        field_head = [*field_names]
        field_head.insert(-1, "QR-code")
        field_head.append("Prolonging")
        thead_th = "\n".join(map(lambda x: f'<th scope="col">{str(x).replace("_", " ").capitalize()}</th>', field_head))

        row_data = [{key: value.value for key, value in row._get_field_value_map(row._meta).items()} for row in rows]
        row_tds = []
        for row in row_data:
            row_field = []
            for key in field_names:
                field_value = row[key]
                css_class = None
                if type(field_value) is datetime.date:
                    if datetime.date.today() >= field_value:
                        css_class = "bg-danger"
                    elif datetime.date.today() + datetime.timedelta(days=7) >= field_value:
                        css_class = "bg-warning"
                    else:
                        css_class = "bg-success"
                if css_class:
                    row_field.append(f'<td class="{css_class}">{str(row[key])}</td>')
                else:
                    row_field.append(f"<td>{str(row[key])}</td>")
            # todo add qr code
            cur_uuid = row["plugin_id"]
            row_field.insert(-1,
                             f'<td><a class="btn btn-sm rounded-pill bg-info" href="personal_cabinet/download_qrcode/{cur_uuid}" download>Download</a></td>')
                             # f'<td><a class="btn btn-sm rounded-pill bg-info" href="personal_cabinet/download_qrcode/{cur_uuid}" target="_blank">Download</a></td>')
            row_field.append(f'<td><a class="btn btn-sm rounded-pill bg-info" href="personal_cabinet/renew/{cur_uuid}">Renew</a></td>')
            row_tds.append("\n".join(row_field))
        tbody = "\n".join(map(lambda x: f"<tr>\n{x}\n</tr>", row_tds))

        return main_html.format(thead_th, tbody)


class LegalUserTable(tables.Table):
    class Meta:
        model = LegalUser
        exclude = ("id", "user",)


class PhysicalUserTable(tables.Table):
    class Meta:
        model = PhysicalUser
        exclude = ("id", "user",)
