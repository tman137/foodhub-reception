import xmlrpc.client


class OdooData:
    def __init__(self, data):
        self.data = data

    def valid(self):
        return self.data and len(self.data) == 1


class MemberRecord(OdooData):
    def can_shop(self):
        return self.data[0]["can_shop"]

    def get_cooperative_status_ids(self):
        return self.data[0]["cooperative_status_ids"]


class CooperativeStatus(OdooData):
    def __init__(self, data):
        super().__init__(data)
        self.mapping = {
            "ok": "Im Plan",
            "alert": "Warnung",
            "suspended": "Gesperrt",
            "extension": "Verlängerunsfrist",
            "unsubscribed": "Abgemeldet",
            "exempted": "Entschuldigt",
            "holiday": "Urlaub",
            "resigning": "Ausgeschieden",
        }

    def get_status(self):
        return self.mapping[self.data[0]["status"]]


class OdooConnector:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password

    def _get_uid(self):
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(self.url))
        return common.authenticate(self.db, self.username, self.password, {})

    def _get_models(self):
        return xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(self.url))

    def get_member(self, barcode):
        uid = self._get_uid()
        models = self._get_models()
        try:
            ids = models.execute_kw(
                self.db,
                uid,
                self.password,
                "res.partner",
                "search",
                [[["barcode", "=", barcode]]],
            )
        except:
            return MemberRecord(None)
        return MemberRecord(
            models.execute_kw(self.db, uid, self.password, "res.partner", "read", [ids])
        )

    def get_cooperative_status(self, ids):
        uid = self._get_uid()
        models = self._get_models()
        return CooperativeStatus(
            models.execute_kw(
                self.db, uid, self.password, "cooperative.status", "read", [ids]
            )
        )

    def get_all_members(self):
        print("fetching members")
        uid = self._get_uid()
        models = self._get_models()
        ids = []
        try:
            ids = models.execute_kw(
                self.db,
                uid,
                self.password,
                "res.partner",
                "search",
                [[["eater", "=", "worker_eater"]]],
            )
        except:
            return None
        return models.execute_kw(
            self.db, uid, self.password, "res.partner", "read", [ids]
        )
