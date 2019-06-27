# Copyright 2019 QuantRocket LLC - All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# To run: python -m unittest discover -s tests/ -p test*.py -t .

import unittest
import os
import pandas as pd
from quantrocket.blotter import read_pnl_csv

INTRADAY_AGGREGATE_RESULTS = {
    'my-strategy': {
        ('AbsExposure', '2019-06-24', '09:30:00'): 0.04696045,
        ('AbsExposure', '2019-06-24', '09:30:01'): 0.0582176,
        ('AbsExposure', '2019-06-24', '09:30:02'): 0.07179037,
        ('AbsExposure', '2019-06-24', '09:30:57'): 0.09748141,
        ('AbsExposure', '2019-06-24', '16:02:02'): 0.07268263,
        ('AbsExposure', '2019-06-24', '16:02:32'): 0.04785271,
        ('AbsExposure', '2019-06-24', '16:02:57'): 0.02569104,
        ('AbsExposure', '2019-06-24', '16:07:54'): 0.0,
        ('AbsExposure', '2019-06-25', '09:30:00'): 0.07527931,
        ('AbsExposure', '2019-06-25', '16:00:01'): 0.05038042,
        ('AbsExposure', '2019-06-25', '16:00:02'): 0.02493937,
        ('AbsExposure', '2019-06-25', '16:02:01'): 0.0,
        ('Account', '2019-06-24', '09:30:00'): 'DU12345',
        ('Account', '2019-06-24', '09:30:01'): 'DU12345',
        ('Account', '2019-06-24', '09:30:02'): 'DU12345',
        ('Account', '2019-06-24', '09:30:57'): 'DU12345',
        ('Account', '2019-06-24', '16:02:02'): 'DU12345',
        ('Account', '2019-06-24', '16:02:32'): 'DU12345',
        ('Account', '2019-06-24', '16:02:57'): 'DU12345',
        ('Account', '2019-06-24', '16:07:54'): 'DU12345',
        ('Account', '2019-06-25', '09:30:00'): 'DU12345',
        ('Account', '2019-06-25', '16:00:01'): 'DU12345',
        ('Account', '2019-06-25', '16:00:02'): 'DU12345',
        ('Account', '2019-06-25', '16:02:01'): 'DU12345',
        ('Commission', '2019-06-24', '09:30:00'): 0.00013768363023328027,
        ('Commission', '2019-06-24', '09:30:01'): 7.868416972425307e-06,
        ('Commission', '2019-06-24', '09:30:02'): 9.487026303954644e-06,
        ('Commission', '2019-06-24', '09:30:57'): 1.4474058363780997e-06,
        ('Commission', '2019-06-24', '16:02:02'): 2.2104505762907916e-06,
        ('Commission', '2019-06-24', '16:02:32'): 1.6174620270380795e-05,
        ('Commission', '2019-06-24', '16:02:57'): 8.287424721657411e-05,
        ('Commission', '2019-06-24', '16:07:54'): 8.264892587397508e-07,
        ('Commission', '2019-06-25', '09:30:00'): 1.6693486908763242e-05,
        ('Commission', '2019-06-25', '16:00:01'): 2.223209635392976e-06,
        ('Commission', '2019-06-25', '16:00:02'): 7.633682434674402e-06,
        ('Commission', '2019-06-25', '16:02:01'): 4.4701827942046415e-06,
        ('CommissionAmount', '2019-06-24', '09:30:00'): 88.4739,
        ('CommissionAmount', '2019-06-24', '09:30:01'): 5.0581,
        ('CommissionAmount', '2019-06-24', '09:30:02'): 6.0986,
        ('CommissionAmount', '2019-06-24', '09:30:57'): 0.9308,
        ('CommissionAmount', '2019-06-24', '16:02:02'): 1.4215,
        ('CommissionAmount', '2019-06-24', '16:02:32'): 10.4016,
        ('CommissionAmount', '2019-06-24', '16:02:57'): 53.2949,
        ('CommissionAmount', '2019-06-24', '16:07:54'): 0.5315,
        ('CommissionAmount', '2019-06-25', '09:30:00'): 10.748,
        ('CommissionAmount', '2019-06-25', '16:00:01'): 1.4314,
        ('CommissionAmount', '2019-06-25', '16:00:02'): 4.9149,
        ('CommissionAmount', '2019-06-25', '16:02:01'): 2.8781,
        ('NetExposure', '2019-06-24', '09:30:00'): -0.04696045,
        ('NetExposure', '2019-06-24', '09:30:01'): -0.0582176,
        ('NetExposure', '2019-06-24', '09:30:02'): -0.07179037,
        ('NetExposure', '2019-06-24', '09:30:57'): -0.09748141,
        ('NetExposure', '2019-06-24', '16:02:02'): -0.07268263,
        ('NetExposure', '2019-06-24', '16:02:32'): -0.04785271,
        ('NetExposure', '2019-06-24', '16:02:57'): -0.02569104,
        ('NetExposure', '2019-06-24', '16:07:54'): 0.0,
        ('NetExposure', '2019-06-25', '09:30:00'): -0.07527931,
        ('NetExposure', '2019-06-25', '16:00:01'): -0.05038042,
        ('NetExposure', '2019-06-25', '16:00:02'): -0.02493937,
        ('NetExposure', '2019-06-25', '16:02:01'): 0.0,
        ('NetLiquidation', '2019-06-24', '09:30:00'): 142588.3734333328,
        ('NetLiquidation', '2019-06-24', '09:30:01'): 142835.7848504977,
        ('NetLiquidation', '2019-06-24', '09:30:02'): 142835.7848504977,
        ('NetLiquidation', '2019-06-24', '09:30:57'): 143081.5577814563,
        ('NetLiquidation', '2019-06-24', '16:02:02'): 143081.5577814563,
        ('NetLiquidation', '2019-06-24', '16:02:32'): 143081.5577814563,
        ('NetLiquidation', '2019-06-24', '16:02:57'): 143081.5577814563,
        ('NetLiquidation', '2019-06-24', '16:07:54'): 143081.5577814563,
        ('NetLiquidation', '2019-06-25', '09:30:00'): 143843.9170163928,
        ('NetLiquidation', '2019-06-25', '16:00:01'): 143843.9170163928,
        ('NetLiquidation', '2019-06-25', '16:00:02'): 143843.9170163928,
        ('NetLiquidation', '2019-06-25', '16:02:01'): 143843.9170163928,
        ('OrderRef', '2019-06-24', '09:30:00'): 'my-strategy',
        ('OrderRef', '2019-06-24', '09:30:01'): 'my-strategy',
        ('OrderRef', '2019-06-24', '09:30:02'): 'my-strategy',
        ('OrderRef', '2019-06-24', '09:30:57'): 'my-strategy',
        ('OrderRef', '2019-06-24', '16:02:02'): 'my-strategy',
        ('OrderRef', '2019-06-24', '16:02:32'): 'my-strategy',
        ('OrderRef', '2019-06-24', '16:02:57'): 'my-strategy',
        ('OrderRef', '2019-06-24', '16:07:54'): 'my-strategy',
        ('OrderRef', '2019-06-25', '09:30:00'): 'my-strategy',
        ('OrderRef', '2019-06-25', '16:00:01'): 'my-strategy',
        ('OrderRef', '2019-06-25', '16:00:02'): 'my-strategy',
        ('OrderRef', '2019-06-25', '16:02:01'): 'my-strategy',
        ('Pnl', '2019-06-24', '09:30:00'): -88.4739,
        ('Pnl', '2019-06-24', '09:30:01'): -5.0581,
        ('Pnl', '2019-06-24', '09:30:02'): -6.0986,
        ('Pnl', '2019-06-24', '09:30:57'): -0.9308,
        ('Pnl', '2019-06-24', '16:02:02'): 340.4585,
        ('Pnl', '2019-06-24', '16:02:32'): 1029.2784,
        ('Pnl', '2019-06-24', '16:02:57'): -809.0687,
        ('Pnl', '2019-06-24', '16:07:54'): -361.4215,
        ('Pnl', '2019-06-25', '09:30:00'): -10.748,
        ('Pnl', '2019-06-25', '16:00:01'): 766.8886,
        ('Pnl', '2019-06-25', '16:00:02'): 264.2851,
        ('Pnl', '2019-06-25', '16:02:01'): 1579.3619,
        ('Return', '2019-06-24', '09:30:00'): -0.00012338,
        ('Return', '2019-06-24', '09:30:01'): -7.05e-06,
        ('Return', '2019-06-24', '09:30:02'): -8.51e-06,
        ('Return', '2019-06-24', '09:30:57'): -1.3e-06,
        ('Return', '2019-06-24', '16:02:02'): 0.0004748,
        ('Return', '2019-06-24', '16:02:32'): 0.00143542,
        ('Return', '2019-06-24', '16:02:57'): -0.00112832,
        ('Return', '2019-06-24', '16:07:54'): -0.00050403,
        ('Return', '2019-06-25', '09:30:00'): -1.492e-05,
        ('Return', '2019-06-25', '16:00:01'): 0.00106425,
        ('Return', '2019-06-25', '16:00:02'): 0.00036676,
        ('Return', '2019-06-25', '16:02:01'): 0.00219177,
        ('TotalHoldings', '2019-06-24', '09:30:00'): 2.0,
        ('TotalHoldings', '2019-06-24', '09:30:01'): 3.0,
        ('TotalHoldings', '2019-06-24', '09:30:02'): 3.0,
        ('TotalHoldings', '2019-06-24', '09:30:57'): 4.0,
        ('TotalHoldings', '2019-06-24', '16:02:02'): 3.0,
        ('TotalHoldings', '2019-06-24', '16:02:32'): 2.0,
        ('TotalHoldings', '2019-06-24', '16:02:57'): 1.0,
        ('TotalHoldings', '2019-06-24', '16:07:54'): 0.0,
        ('TotalHoldings', '2019-06-25', '09:30:00'): 3.0,
        ('TotalHoldings', '2019-06-25', '16:00:01'): 2.0,
        ('TotalHoldings', '2019-06-25', '16:00:02'): 1.0,
        ('TotalHoldings', '2019-06-25', '16:02:01'): 0.0,
        ('Turnover', '2019-06-24', '09:30:00'): 0.0469604542140948,
        ('Turnover', '2019-06-24', '09:30:01'): 0.011257145696517867,
        ('Turnover', '2019-06-24', '09:30:02'): 0.013572770371361662,
        ('Turnover', '2019-06-24', '09:30:57'): 0.02569104439785384,
        ('Turnover', '2019-06-24', '16:02:02'): 0.024798788931251575,
        ('Turnover', '2019-06-24', '16:02:32'): 0.02482991606787953,
        ('Turnover', '2019-06-24', '16:02:57'): 0.02216166528284323,
        ('Turnover', '2019-06-24', '16:07:54'): 0.02569104439785384,
        ('Turnover', '2019-06-25', '09:30:00'): 0.07527930520305026,
        ('Turnover', '2019-06-25', '16:00:01'): 0.02489888536596387,
        ('Turnover', '2019-06-25', '16:00:02'): 0.025441053646071972,
        ('Turnover', '2019-06-25', '16:02:01'): 0.024939366191014428}
}

INTRADAY_DETAILED_RESULTS = {
    'CBL(5474)': {
        ('AbsExposure', '2019-06-24', '09:30:00'): 0.02216167,
        ('AbsExposure', '2019-06-24', '09:30:01'): 0.02216167,
        ('AbsExposure', '2019-06-24', '09:30:02'): 0.02216167,
        ('AbsExposure', '2019-06-24', '09:30:57'): 0.02216167,
        ('AbsExposure', '2019-06-24', '16:02:02'): 0.02216167,
        ('AbsExposure', '2019-06-24', '16:02:32'): 0.02216167,
        ('AbsExposure', '2019-06-24', '16:02:57'): 0.0,
        ('AbsExposure', '2019-06-24', '16:07:54'): 0.0,
        ('AbsExposure', '2019-06-25', '09:30:00'): 0.0,
        ('AbsExposure', '2019-06-25', '16:00:01'): 0.0,
        ('AbsExposure', '2019-06-25', '16:00:02'): 0.0,
        ('AbsExposure', '2019-06-25', '16:02:01'): 0.0,
        ('Commission', '2019-06-24', '09:30:00'): 0.00012081498820718027,
        ('Commission', '2019-06-24', '09:30:01'): 0.0,
        ('Commission', '2019-06-24', '09:30:02'): 0.0,
        ('Commission', '2019-06-24', '09:30:57'): 0.0,
        ('Commission', '2019-06-24', '16:02:02'): 0.0,
        ('Commission', '2019-06-24', '16:02:32'): 0.0,
        ('Commission', '2019-06-24', '16:02:57'): 7.432426675057977e-05,
        ('Commission', '2019-06-24', '16:07:54'): 0.0,
        ('Commission', '2019-06-25', '09:30:00'): 0.0,
        ('Commission', '2019-06-25', '16:00:01'): 0.0,
        ('Commission', '2019-06-25', '16:00:02'): 0.0,
        ('Commission', '2019-06-25', '16:02:01'): 0.0,
        ('CommissionAmount', '2019-06-24', '09:30:00'): 86.6315,
        ('CommissionAmount', '2019-06-24', '09:30:01'): 0.0,
        ('CommissionAmount', '2019-06-24', '09:30:02'): 0.0,
        ('CommissionAmount', '2019-06-24', '09:30:57'): 0.0,
        ('CommissionAmount', '2019-06-24', '16:02:02'): 0.0,
        ('CommissionAmount', '2019-06-24', '16:02:32'): 0.0,
        ('CommissionAmount', '2019-06-24', '16:02:57'): 53.2949,
        ('CommissionAmount', '2019-06-24', '16:07:54'): 0.0,
        ('CommissionAmount', '2019-06-25', '09:30:00'): 0.0,
        ('CommissionAmount', '2019-06-25', '16:00:01'): 0.0,
        ('CommissionAmount', '2019-06-25', '16:00:02'): 0.0,
        ('CommissionAmount', '2019-06-25', '16:02:01'): 0.0,
        ('NetExposure', '2019-06-24', '09:30:00'): -0.02216167,
        ('NetExposure', '2019-06-24', '09:30:01'): -0.02216167,
        ('NetExposure', '2019-06-24', '09:30:02'): -0.02216167,
        ('NetExposure', '2019-06-24', '09:30:57'): -0.02216167,
        ('NetExposure', '2019-06-24', '16:02:02'): -0.02216167,
        ('NetExposure', '2019-06-24', '16:02:32'): -0.02216167,
        ('NetExposure', '2019-06-24', '16:02:57'): 0.0,
        ('NetExposure', '2019-06-24', '16:07:54'): 0.0,
        ('NetExposure', '2019-06-25', '09:30:00'): 0.0,
        ('NetExposure', '2019-06-25', '16:00:01'): 0.0,
        ('NetExposure', '2019-06-25', '16:00:02'): 0.0,
        ('NetExposure', '2019-06-25', '16:02:01'): 0.0,
        ('NetLiquidation', '2019-06-24', '09:30:00'): 717059.21,
        ('NetLiquidation', '2019-06-24', '09:30:01'): 717059.21,
        ('NetLiquidation', '2019-06-24', '09:30:02'): 717059.21,
        ('NetLiquidation', '2019-06-24', '09:30:57'): 717059.21,
        ('NetLiquidation', '2019-06-24', '16:02:02'): 717059.21,
        ('NetLiquidation', '2019-06-24', '16:02:32'): 717059.21,
        ('NetLiquidation', '2019-06-24', '16:02:57'): 717059.21,
        ('NetLiquidation', '2019-06-24', '16:07:54'): 717059.21,
        ('NetLiquidation', '2019-06-25', '09:30:00'): 720588.08,
        ('NetLiquidation', '2019-06-25', '16:00:01'): 720588.08,
        ('NetLiquidation', '2019-06-25', '16:00:02'): 720588.08,
        ('NetLiquidation', '2019-06-25', '16:02:01'): 720588.08,
        ('Pnl', '2019-06-24', '09:30:00'): -86.6315,
        ('Pnl', '2019-06-24', '09:30:01'): 0.0,
        ('Pnl', '2019-06-24', '09:30:02'): 0.0,
        ('Pnl', '2019-06-24', '09:30:57'): 0.0,
        ('Pnl', '2019-06-24', '16:02:02'): 0.0,
        ('Pnl', '2019-06-24', '16:02:32'): 0.0,
        ('Pnl', '2019-06-24', '16:02:57'): -809.0687,
        ('Pnl', '2019-06-24', '16:07:54'): 0.0,
        ('Pnl', '2019-06-25', '09:30:00'): 0.0,
        ('Pnl', '2019-06-25', '16:00:01'): 0.0,
        ('Pnl', '2019-06-25', '16:00:02'): 0.0,
        ('Pnl', '2019-06-25', '16:02:01'): 0.0,
        ('PositionQuantity', '2019-06-24', '09:30:00'): -16647.0,
        ('PositionQuantity', '2019-06-24', '09:30:01'): -16647.0,
        ('PositionQuantity', '2019-06-24', '09:30:02'): -16647.0,
        ('PositionQuantity', '2019-06-24', '09:30:57'): -16647.0,
        ('PositionQuantity', '2019-06-24', '16:02:02'): -16647.0,
        ('PositionQuantity', '2019-06-24', '16:02:32'): -16647.0,
        ('PositionQuantity', '2019-06-24', '16:02:57'): 0.0,
        ('PositionQuantity', '2019-06-24', '16:07:54'): 0.0,
        ('PositionQuantity', '2019-06-25', '09:30:00'): 0.0,
        ('PositionQuantity', '2019-06-25', '16:00:01'): 0.0,
        ('PositionQuantity', '2019-06-25', '16:00:02'): 0.0,
        ('PositionQuantity', '2019-06-25', '16:02:01'): 0.0,
        ('PositionValue', '2019-06-24', '09:30:00'): -15891.2262,
        ('PositionValue', '2019-06-24', '09:30:01'): -15891.2262,
        ('PositionValue', '2019-06-24', '09:30:02'): -15891.2262,
        ('PositionValue', '2019-06-24', '09:30:57'): -15891.2262,
        ('PositionValue', '2019-06-24', '16:02:02'): -15891.2262,
        ('PositionValue', '2019-06-24', '16:02:32'): -15891.2262,
        ('PositionValue', '2019-06-24', '16:02:57'): 0.0,
        ('PositionValue', '2019-06-24', '16:07:54'): 0.0,
        ('PositionValue', '2019-06-25', '09:30:00'): 0.0,
        ('PositionValue', '2019-06-25', '16:00:01'): 0.0,
        ('PositionValue', '2019-06-25', '16:00:02'): 0.0,
        ('PositionValue', '2019-06-25', '16:02:01'): 0.0,
        ('Price', '2019-06-24', '09:30:00'): 0.95,
        ('Price', '2019-06-24', '09:30:01'): 0.95,
        ('Price', '2019-06-24', '09:30:02'): 0.95,
        ('Price', '2019-06-24', '09:30:57'): 0.95,
        ('Price', '2019-06-24', '16:02:02'): 0.95,
        ('Price', '2019-06-24', '16:02:32'): 0.95,
        ('Price', '2019-06-24', '16:02:57'): 1.0,
        ('Price', '2019-06-24', '16:07:54'): 1.0,
        ('Price', '2019-06-25', '09:30:00'): 1.0,
        ('Price', '2019-06-25', '16:00:01'): 1.0,
        ('Price', '2019-06-25', '16:00:02'): 1.0,
        ('Price', '2019-06-25', '16:02:01'): 1.0,
        ('Return', '2019-06-24', '09:30:00'): -0.001,
        ('Return', '2019-06-24', '09:30:01'): 0.0,
        ('Return', '2019-06-24', '09:30:02'): 0.0,
        ('Return', '2019-06-24', '09:30:57'): 0.0,
        ('Return', '2019-06-24', '16:02:02'): 0.01,
        ('Return', '2019-06-24', '16:02:32'): 0.01,
        ('Return', '2019-06-24', '16:02:57'): -0.0011,
        ('Return', '2019-06-24', '16:07:54'): 0.0,
        ('Return', '2019-06-25', '09:30:00'): 0.0,
        ('Return', '2019-06-25', '16:00:01'): 0.0,
        ('Return', '2019-06-25', '16:00:02'): 0.0,
        ('Return', '2019-06-25', '16:02:01'): 0.0,
        ('TotalHoldings', '2019-06-24', '09:30:00'): 1.0,
        ('TotalHoldings', '2019-06-24', '09:30:01'): 1.0,
        ('TotalHoldings', '2019-06-24', '09:30:02'): 1.0,
        ('TotalHoldings', '2019-06-24', '09:30:57'): 1.0,
        ('TotalHoldings', '2019-06-24', '16:02:02'): 1.0,
        ('TotalHoldings', '2019-06-24', '16:02:32'): 1.0,
        ('TotalHoldings', '2019-06-24', '16:02:57'): 0.0,
        ('TotalHoldings', '2019-06-24', '16:07:54'): 0.0,
        ('TotalHoldings', '2019-06-25', '09:30:00'): 0.0,
        ('TotalHoldings', '2019-06-25', '16:00:01'): 0.0,
        ('TotalHoldings', '2019-06-25', '16:00:02'): 0.0,
        ('TotalHoldings', '2019-06-25', '16:02:01'): 0.0,
        ('Turnover', '2019-06-24', '09:30:00'): 0.02216167,
        ('Turnover', '2019-06-24', '09:30:01'): 0.0,
        ('Turnover', '2019-06-24', '09:30:02'): 0.0,
        ('Turnover', '2019-06-24', '09:30:57'): 0.0,
        ('Turnover', '2019-06-24', '16:02:02'): 0.0,
        ('Turnover', '2019-06-24', '16:02:32'): 0.0,
        ('Turnover', '2019-06-24', '16:02:57'): 0.02216167,
        ('Turnover', '2019-06-24', '16:07:54'): 0.0,
        ('Turnover', '2019-06-25', '09:30:00'): 0.0,
        ('Turnover', '2019-06-25', '16:00:01'): 0.0,
        ('Turnover', '2019-06-25', '16:00:02'): 0.0,
        ('Turnover', '2019-06-25', '16:02:01'): 0.0},
    'KFY(6477845)': {
        ('AbsExposure', '2019-06-24', '09:30:00'): 0.02479879,
        ('AbsExposure', '2019-06-24', '09:30:01'): 0.02479879,
        ('AbsExposure', '2019-06-24', '09:30:02'): 0.02479879,
        ('AbsExposure', '2019-06-24', '09:30:57'): 0.02479879,
        ('AbsExposure', '2019-06-24', '16:02:02'): 0.0,
        ('AbsExposure', '2019-06-24', '16:02:32'): 0.0,
        ('AbsExposure', '2019-06-24', '16:02:57'): 0.0,
        ('AbsExposure', '2019-06-24', '16:07:54'): 0.0,
        ('AbsExposure', '2019-06-25', '09:30:00'): 0.0,
        ('AbsExposure', '2019-06-25', '16:00:01'): 0.0,
        ('AbsExposure', '2019-06-25', '16:00:02'): 0.0,
        ('AbsExposure', '2019-06-25', '16:02:01'): 0.0,
        ('Commission', '2019-06-24', '09:30:00'): 2.569383356780258e-06,
        ('Commission', '2019-06-24', '09:30:01'): 0.0,
        ('Commission', '2019-06-24', '09:30:02'): 0.0,
        ('Commission', '2019-06-24', '09:30:57'): 0.0,
        ('Commission', '2019-06-24', '16:02:02'): 1.9824025410677034e-06,
        ('Commission', '2019-06-24', '16:02:32'): 0.0,
        ('Commission', '2019-06-24', '16:02:57'): 0.0,
        ('Commission', '2019-06-24', '16:07:54'): 0.0,
        ('Commission', '2019-06-25', '09:30:00'): 0.0,
        ('Commission', '2019-06-25', '16:00:01'): 0.0,
        ('Commission', '2019-06-25', '16:00:02'): 0.0,
        ('Commission', '2019-06-25', '16:02:01'): 0.0,
        ('CommissionAmount', '2019-06-24', '09:30:00'): 1.8424,
        ('CommissionAmount', '2019-06-24', '09:30:01'): 0.0,
        ('CommissionAmount', '2019-06-24', '09:30:02'): 0.0,
        ('CommissionAmount', '2019-06-24', '09:30:57'): 0.0,
        ('CommissionAmount', '2019-06-24', '16:02:02'): 1.4215,
        ('CommissionAmount', '2019-06-24', '16:02:32'): 0.0,
        ('CommissionAmount', '2019-06-24', '16:02:57'): 0.0,
        ('CommissionAmount', '2019-06-24', '16:07:54'): 0.0,
        ('CommissionAmount', '2019-06-25', '09:30:00'): 0.0,
        ('CommissionAmount', '2019-06-25', '16:00:01'): 0.0,
        ('CommissionAmount', '2019-06-25', '16:00:02'): 0.0,
        ('CommissionAmount', '2019-06-25', '16:02:01'): 0.0,
        ('NetExposure', '2019-06-24', '09:30:00'): -0.02479879,
        ('NetExposure', '2019-06-24', '09:30:01'): -0.02479879,
        ('NetExposure', '2019-06-24', '09:30:02'): -0.02479879,
        ('NetExposure', '2019-06-24', '09:30:57'): -0.02479879,
        ('NetExposure', '2019-06-24', '16:02:02'): 0.0,
        ('NetExposure', '2019-06-24', '16:02:32'): 0.0,
        ('NetExposure', '2019-06-24', '16:02:57'): 0.0,
        ('NetExposure', '2019-06-24', '16:07:54'): 0.0,
        ('NetExposure', '2019-06-25', '09:30:00'): 0.0,
        ('NetExposure', '2019-06-25', '16:00:01'): 0.0,
        ('NetExposure', '2019-06-25', '16:00:02'): 0.0,
        ('NetExposure', '2019-06-25', '16:02:01'): 0.0,
        ('NetLiquidation', '2019-06-24', '09:30:00'): 717059.21,
        ('NetLiquidation', '2019-06-24', '09:30:01'): 717059.21,
        ('NetLiquidation', '2019-06-24', '09:30:02'): 717059.21,
        ('NetLiquidation', '2019-06-24', '09:30:57'): 717059.21,
        ('NetLiquidation', '2019-06-24', '16:02:02'): 717059.21,
        ('NetLiquidation', '2019-06-24', '16:02:32'): 717059.21,
        ('NetLiquidation', '2019-06-24', '16:02:57'): 717059.21,
        ('NetLiquidation', '2019-06-24', '16:07:54'): 717059.21,
        ('NetLiquidation', '2019-06-25', '09:30:00'): 720588.08,
        ('NetLiquidation', '2019-06-25', '16:00:01'): 720588.08,
        ('NetLiquidation', '2019-06-25', '16:00:02'): 720588.08,
        ('NetLiquidation', '2019-06-25', '16:02:01'): 720588.08,
        ('Pnl', '2019-06-24', '09:30:00'): -1.8424,
        ('Pnl', '2019-06-24', '09:30:01'): 0.0,
        ('Pnl', '2019-06-24', '09:30:02'): 0.0,
        ('Pnl', '2019-06-24', '09:30:57'): 0.0,
        ('Pnl', '2019-06-24', '16:02:02'): 340.4585,
        ('Pnl', '2019-06-24', '16:02:32'): 0.0,
        ('Pnl', '2019-06-24', '16:02:57'): 0.0,
        ('Pnl', '2019-06-24', '16:07:54'): 0.0,
        ('Pnl', '2019-06-25', '09:30:00'): 0.0,
        ('Pnl', '2019-06-25', '16:00:01'): 0.0,
        ('Pnl', '2019-06-25', '16:00:02'): 0.0,
        ('Pnl', '2019-06-25', '16:02:01'): 0.0,
        ('PositionQuantity', '2019-06-24', '09:30:00'): -444.0,
        ('PositionQuantity', '2019-06-24', '09:30:01'): -444.0,
        ('PositionQuantity', '2019-06-24', '09:30:02'): -444.0,
        ('PositionQuantity', '2019-06-24', '09:30:57'): -444.0,
        ('PositionQuantity', '2019-06-24', '16:02:02'): 0.0,
        ('PositionQuantity', '2019-06-24', '16:02:32'): 0.0,
        ('PositionQuantity', '2019-06-24', '16:02:57'): 0.0,
        ('PositionQuantity', '2019-06-24', '16:07:54'): 0.0,
        ('PositionQuantity', '2019-06-25', '09:30:00'): 0.0,
        ('PositionQuantity', '2019-06-25', '16:00:01'): 0.0,
        ('PositionQuantity', '2019-06-25', '16:00:02'): 0.0,
        ('PositionQuantity', '2019-06-25', '16:02:01'): 0.0,
        ('PositionValue', '2019-06-24', '09:30:00'): -17782.2,
        ('PositionValue', '2019-06-24', '09:30:01'): -17782.2,
        ('PositionValue', '2019-06-24', '09:30:02'): -17782.2,
        ('PositionValue', '2019-06-24', '09:30:57'): -17782.2,
        ('PositionValue', '2019-06-24', '16:02:02'): 0.0,
        ('PositionValue', '2019-06-24', '16:02:32'): 0.0,
        ('PositionValue', '2019-06-24', '16:02:57'): 0.0,
        ('PositionValue', '2019-06-24', '16:07:54'): 0.0,
        ('PositionValue', '2019-06-25', '09:30:00'): 0.0,
        ('PositionValue', '2019-06-25', '16:00:01'): 0.0,
        ('PositionValue', '2019-06-25', '16:00:02'): 0.0,
        ('PositionValue', '2019-06-25', '16:02:01'): 0.0,
        ('Price', '2019-06-24', '09:30:00'): 40.05,
        ('Price', '2019-06-24', '09:30:01'): 40.05,
        ('Price', '2019-06-24', '09:30:02'): 40.05,
        ('Price', '2019-06-24', '09:30:57'): 40.05,
        ('Price', '2019-06-24', '16:02:02'): 39.28,
        ('Price', '2019-06-24', '16:02:32'): 39.28,
        ('Price', '2019-06-24', '16:02:57'): 39.28,
        ('Price', '2019-06-24', '16:07:54'): 39.28,
        ('Price', '2019-06-25', '09:30:00'): 39.28,
        ('Price', '2019-06-25', '16:00:01'): 39.28,
        ('Price', '2019-06-25', '16:00:02'): 39.28,
        ('Price', '2019-06-25', '16:02:01'): 39.28,
        ('Return', '2019-06-24', '09:30:00'): -2.57e-06,
        ('Return', '2019-06-24', '09:30:01'): 0.0,
        ('Return', '2019-06-24', '09:30:02'): 0.0,
        ('Return', '2019-06-24', '09:30:57'): 0.0,
        ('Return', '2019-06-24', '16:02:02'): 0.0047,
        ('Return', '2019-06-24', '16:02:32'): 0.0,
        ('Return', '2019-06-24', '16:02:57'): 0.0,
        ('Return', '2019-06-24', '16:07:54'): 0.0,
        ('Return', '2019-06-25', '09:30:00'): 0.0,
        ('Return', '2019-06-25', '16:00:01'): 0.0,
        ('Return', '2019-06-25', '16:00:02'): 0.0,
        ('Return', '2019-06-25', '16:02:01'): 0.0,
        ('TotalHoldings', '2019-06-24', '09:30:00'): 1.0,
        ('TotalHoldings', '2019-06-24', '09:30:01'): 1.0,
        ('TotalHoldings', '2019-06-24', '09:30:02'): 1.0,
        ('TotalHoldings', '2019-06-24', '09:30:57'): 1.0,
        ('TotalHoldings', '2019-06-24', '16:02:02'): 0.0,
        ('TotalHoldings', '2019-06-24', '16:02:32'): 0.0,
        ('TotalHoldings', '2019-06-24', '16:02:57'): 0.0,
        ('TotalHoldings', '2019-06-24', '16:07:54'): 0.0,
        ('TotalHoldings', '2019-06-25', '09:30:00'): 0.0,
        ('TotalHoldings', '2019-06-25', '16:00:01'): 0.0,
        ('TotalHoldings', '2019-06-25', '16:00:02'): 0.0,
        ('TotalHoldings', '2019-06-25', '16:02:01'): 0.0,
        ('Turnover', '2019-06-24', '09:30:00'): 0.02479879,
        ('Turnover', '2019-06-24', '09:30:01'): 0.0,
        ('Turnover', '2019-06-24', '09:30:02'): 0.0,
        ('Turnover', '2019-06-24', '09:30:57'): 0.0,
        ('Turnover', '2019-06-24', '16:02:02'): 0.02479879,
        ('Turnover', '2019-06-24', '16:02:32'): 0.0,
        ('Turnover', '2019-06-24', '16:02:57'): 0.0,
        ('Turnover', '2019-06-24', '16:07:54'): 0.0,
        ('Turnover', '2019-06-25', '09:30:00'): 0.0,
        ('Turnover', '2019-06-25', '16:00:01'): 0.0,
        ('Turnover', '2019-06-25', '16:00:02'): 0.0,
        ('Turnover', '2019-06-25', '16:02:01'): 0.0}}

class ReadPnlCsvTestCase(unittest.TestCase):
    """
    Test cases for `quantrocket.blotter.read_pnl_csv`.
    """

    def tearDown(self):
        if os.path.exists("results.csv"):
            os.remove("results.csv")

    def test_intraday_aggregate(self):

        results = pd.DataFrame.from_dict(INTRADAY_AGGREGATE_RESULTS)
        results.index.set_names(["Field","Date", "Time"], inplace=True)
        results.to_csv("results.csv")

        results = read_pnl_csv("results.csv")

        results = results.reset_index()
        results.loc[:, "Date"] = results.Date.dt.strftime("%Y-%m-%d")
        results = results.set_index(["Field", "Date", "Time"])

        self.assertDictEqual(
            results.to_dict(),
            INTRADAY_AGGREGATE_RESULTS
        )

    def test_intraday_detailed(self):

        self.maxDiff = None
        results = pd.DataFrame.from_dict(INTRADAY_DETAILED_RESULTS)
        results.index.set_names(["Field","Date", "Time"], inplace=True)
        results.to_csv("results.csv")

        results = read_pnl_csv("results.csv")

        results = results.reset_index()
        results.loc[:, "Date"] = results.Date.dt.strftime("%Y-%m-%d")
        results = results.set_index(["Field", "Date", "Time"])

        results = results.where(results.notnull(), None)

        self.assertDictEqual(
            results.to_dict(),
            INTRADAY_DETAILED_RESULTS
        )
