#!/usr/bin/env python

# -*- coding: utf-8 -*-
#
# Copyright 2012-2015 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os,sys,datetime,json
import luigi
# from pprint import pprint

# import components for bolflow
from plugins import *


__author__ = 'jmrodriguezc'

class config(luigi.Task):
    config = luigi.Parameter()
    pid    = os.getpid()
    date   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    data = {}

    def output(self):
        '''
        Returns the config file for the workflow.
        '''
        self.data = json.load( open(self.config) )
        self.data['wsdir']  = self.data['wsdir'] + '/bolflow_' + self.date
        self.data['logdir'] = self.data['wsdir'] + '/log'
        self.data['config'] = self.data['wsdir'] +'/config.json'
        return luigi.LocalTarget(self.data['config'])

    def run(self):
        '''
        Create config file for the current job of workflow
        '''
        # TODO!! check config file
        # try:
        #     pass
        # except expression as identifier:
        #     pass

        # create needed dirs
        os.makedirs(self.data['wsdir'])
        os.makedirs(self.data['logdir'])

        # create config
        with self.output().open('w') as f:
            json.dump(self.data, f, indent=1)

    # @config.event_handler(luigi.Event.FAILURE)
    # def mourn_failure(task, exception):
    #     '''
    #     Will be called directly after a failed execution of `run` on any MyTask subclass
    #     '''
    #     print(task)
    #     print(exception)


if __name__ == '__main__':
    luigi.run()
