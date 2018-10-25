#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright (c) 2014 Mozilla Corporation

from lib.alerttask import AlertTask
from mozdef_util.query_models import SearchQuery, TermMatch


class ldapAdd(AlertTask):
    def main(self):
        search_query = SearchQuery(minutes=15)

        search_query.add_must([
            TermMatch('category', 'ldapChange'),
            TermMatch('details.changetype', 'add')
        ])

        self.filtersManual(search_query)

        # Search events
        self.searchEventsSimple()
        self.walkEvents()

    # Set alert properties
    def onEvent(self, event):
        category = 'ldap'
        tags = ['ldap']
        severity = 'INFO'
        summary='{0} added {1}'.format(event['_source']['details']['actor'], event['_source']['details']['dn'])

        # Create the alert object based on these properties
        return self.createAlertDict(summary, category, tags, [event], severity)
