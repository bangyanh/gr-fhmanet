#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: DPSK Transceiver MAC
# Author: Jason Noble
# Description: bladeRF MAC and modem based on J. Malbury's Simple MAC.
# Generated: Fri Jan  1 17:19:17 2016
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from dpsk_radio import dpsk_radio  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import fhmanet
import mac
import osmosdr
import pmt
import time


class dpsk_fhmanet_trx(gr.top_block):

    def __init__(self, ampl=0.7, arq_timeout=.1*0 + 0.04, broadcast_interval=1, cen_freq=2442500000, dest_addr=1, fh_rate=10, max_arq_attempts=5 * 2, mtu=128, port="12345", radio_addr=0, rate=1e6, samps_per_sym=4):
        gr.top_block.__init__(self, "DPSK Transceiver MAC")

        ##################################################
        # Parameters
        ##################################################
        self.ampl = ampl
        self.arq_timeout = arq_timeout
        self.broadcast_interval = broadcast_interval
        self.cen_freq = cen_freq
        self.dest_addr = dest_addr
        self.fh_rate = fh_rate
        self.max_arq_attempts = max_arq_attempts
        self.mtu = mtu
        self.port = port
        self.radio_addr = radio_addr
        self.rate = rate
        self.samps_per_sym = samps_per_sym

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = rate
        self.hop_rate = hop_rate = fh_rate
        self.channel_width = channel_width = 50000
        self.center_freq = center_freq = cen_freq

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "bladerf=0" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "bladerf=0" )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(center_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(10, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        self.mac_virtual_channel_encoder_0 = mac.virtual_channel_encoder(dest_addr, True,mtu=mtu,
        chan_id=0,
        prepend_dummy=False,
        )
        self.mac_virtual_channel_decoder_0 = mac.virtual_channel_decoder(3, [0,1])
        self.fhmanet_mac_0 = fhmanet.fhmanet_mac(
        		radio_addr,
        		0.01,
        		10,
        		2.0,
        		True,
        		0.05,
        		node_expiry_delay=10.0,
        		expire_on_arq_failure=False,
        		only_send_if_alive=False,
        		prepend_dummy=False)
        	
        self.fhmanet_fh_channel_message_strobe_0 = Template error: fhmanet.fh_channel_message_strobe(
        		$msg, 
        		$period_ms,
        		$msg2,
        		$center_freq, 
        		$channel_width, 
        		$num_channels, 
        		$sequence_length, 
        		$freq_offset, 
        		$tx_security_key)
        	
            cannot find 'msg'
        self.dpsk_radio_0 = dpsk_radio(
            access_code_threshold=0 + 12 + 4*0,
            ampl=ampl,
            rate=samp_rate,
            samps_per_sym=samps_per_sym)
          
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_SERVER", "", port, mtu, False)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("T"), 1)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.fhmanet_mac_0, 'ctrl_in'))    
        self.msg_connect((self.blocks_socket_pdu_0, 'pdus'), (self.mac_virtual_channel_encoder_0, 'in'))    
        self.msg_connect((self.dpsk_radio_0, 'msg_out'), (self.fhmanet_mac_0, 'from_radio'))    
        self.msg_connect((self.fhmanet_fh_channel_message_strobe_0, 'freq_out'), (self.dpsk_radio_0, 'freq_in'))    
        self.msg_connect((self.fhmanet_fh_channel_message_strobe_0, 'offset_freq_out'), (self.dpsk_radio_0, 'offset_freq_in'))    
        self.msg_connect((self.fhmanet_mac_0, 'to_radio'), (self.dpsk_radio_0, 'msg_in'))    
        self.msg_connect((self.fhmanet_mac_0, 'to_app'), (self.mac_virtual_channel_decoder_0, 'in'))    
        self.msg_connect((self.mac_virtual_channel_decoder_0, 'out0'), (self.blocks_socket_pdu_0, 'pdus'))    
        self.msg_connect((self.mac_virtual_channel_encoder_0, 'out'), (self.fhmanet_mac_0, 'from_app_arq'))    
        self.connect((self.dpsk_radio_0, 0), (self.osmosdr_sink_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.dpsk_radio_0, 0))    

    def get_ampl(self):
        return self.ampl

    def set_ampl(self, ampl):
        self.ampl = ampl
        self.dpsk_radio_0.set_ampl(self.ampl)

    def get_arq_timeout(self):
        return self.arq_timeout

    def set_arq_timeout(self, arq_timeout):
        self.arq_timeout = arq_timeout

    def get_broadcast_interval(self):
        return self.broadcast_interval

    def set_broadcast_interval(self, broadcast_interval):
        self.broadcast_interval = broadcast_interval

    def get_cen_freq(self):
        return self.cen_freq

    def set_cen_freq(self, cen_freq):
        self.cen_freq = cen_freq
        self.set_center_freq(self.cen_freq)

    def get_dest_addr(self):
        return self.dest_addr

    def set_dest_addr(self, dest_addr):
        self.dest_addr = dest_addr

    def get_fh_rate(self):
        return self.fh_rate

    def set_fh_rate(self, fh_rate):
        self.fh_rate = fh_rate
        self.set_hop_rate(self.fh_rate)

    def get_max_arq_attempts(self):
        return self.max_arq_attempts

    def set_max_arq_attempts(self, max_arq_attempts):
        self.max_arq_attempts = max_arq_attempts

    def get_mtu(self):
        return self.mtu

    def set_mtu(self, mtu):
        self.mtu = mtu

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_radio_addr(self):
        return self.radio_addr

    def set_radio_addr(self, radio_addr):
        self.radio_addr = radio_addr

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate
        self.set_samp_rate(self.rate)

    def get_samps_per_sym(self):
        return self.samps_per_sym

    def set_samps_per_sym(self, samps_per_sym):
        self.samps_per_sym = samps_per_sym
        self.dpsk_radio_0.set_samps_per_sym(self.samps_per_sym)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
        self.dpsk_radio_0.set_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_hop_rate(self):
        return self.hop_rate

    def set_hop_rate(self, hop_rate):
        self.hop_rate = hop_rate

    def get_channel_width(self):
        return self.channel_width

    def set_channel_width(self, channel_width):
        self.channel_width = channel_width

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.osmosdr_sink_0.set_center_freq(self.center_freq, 0)
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)


def argument_parser():
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option(
        "", "--ampl", dest="ampl", type="eng_float", default=eng_notation.num_to_str(0.7),
        help="Set TX BB amp [default=%default]")
    parser.add_option(
        "-t", "--arq-timeout", dest="arq_timeout", type="eng_float", default=eng_notation.num_to_str(.1*0 + 0.04),
        help="Set ARQ timeout [default=%default]")
    parser.add_option(
        "-b", "--broadcast-interval", dest="broadcast_interval", type="eng_float", default=eng_notation.num_to_str(1),
        help="Set Broadcast Interval [default=%default]")
    parser.add_option(
        "-c", "--cen-freq", dest="cen_freq", type="eng_float", default=eng_notation.num_to_str(2442500000),
        help="Set Center Frequency [default=%default]")
    parser.add_option(
        "-d", "--dest-addr", dest="dest_addr", type="intx", default=1,
        help="Set Destination address [default=%default]")
    parser.add_option(
        "-h", "--fh-rate", dest="fh_rate", type="eng_float", default=eng_notation.num_to_str(10),
        help="Set Hop rate [default=%default]")
    parser.add_option(
        "", "--max-arq-attempts", dest="max_arq_attempts", type="intx", default=5 * 2,
        help="Set Max ARQ attempts [default=%default]")
    parser.add_option(
        "", "--mtu", dest="mtu", type="intx", default=128,
        help="Set TCP Socket MTU [default=%default]")
    parser.add_option(
        "", "--port", dest="port", type="string", default="12345",
        help="Set TCP port [default=%default]")
    parser.add_option(
        "-l", "--radio-addr", dest="radio_addr", type="intx", default=0,
        help="Set Local address [default=%default]")
    parser.add_option(
        "-r", "--rate", dest="rate", type="eng_float", default=eng_notation.num_to_str(1e6),
        help="Set Sample rate [default=%default]")
    parser.add_option(
        "", "--samps-per-sym", dest="samps_per_sym", type="intx", default=4,
        help="Set Samples/symbol [default=%default]")
    return parser


def main(top_block_cls=dpsk_fhmanet_trx, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(ampl=options.ampl, arq_timeout=options.arq_timeout, broadcast_interval=options.broadcast_interval, cen_freq=options.cen_freq, dest_addr=options.dest_addr, fh_rate=options.fh_rate, max_arq_attempts=options.max_arq_attempts, mtu=options.mtu, port=options.port, radio_addr=options.radio_addr, rate=options.rate, samps_per_sym=options.samps_per_sym)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()