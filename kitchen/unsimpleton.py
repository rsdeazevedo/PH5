#!/usr/bin/env pnpython4
#
#   Rename nodal fcnt file names to RL_S.0.x.rg16 filename format.
#
#   Input: List of files to rename in a file (one per line), output directory for links
#
#   Usage: unsimpleton list_of_files out_directory
#
#   Steve Azevedo, August 2016
#
import sys, os
sys.path.append (os.path.join (os.environ["KX"], "apps", "pn4"))
import SegdReader

PROG_VERSION = "2016.190 Developmental"

def print_container (container) :
    keys = container.keys ()
    for k in keys :
        print k, container[k]
        
    print '-' * 80

def general_headers (sd) :
    sd.process_general_headers ()
    #print '*' * 80
    #print sd.infile
    #print '*' * 80
    #print "*** General Header Block 1 ***"
    #print_container (sd.reel_headers.general_header_block_1)
    #print "*** General Header Block 2 ***"
    #print_container (sd.reel_headers.general_header_block_2)
    
def channel_set_descriptors (sd) :
    #print "*** Channel Set Descriptor(s): ***"
    sd.process_channel_set_descriptors ()
    #i = 1
    #for c in sd.reel_headers.channel_set_descriptor :
        #print i; i += 1
        #print_container (c)
        
def extended_headers (sd) :
    #print "*** Extended Headers ***"
    sd.process_extended_headers ()
    #n = sd.extended_header_blocks
    #if n > 0 :
        #print_container (sd.reel_headers.extended_header_1)
        #n -= 1
    #else : return
    #if n > 0 :
        #print 2
        #print_container (sd.reel_headers.extended_header_2)
        #n -= 1
    #else : return
    #if n > 0 :
        #print 3
        #print_container (sd.reel_headers.extended_header_3)
        
    #i = 1
    #for c in sd.reel_headers.extended_header_4 :
        #print i; i += 1
        #print_container (c)
        
def external_header (sd) :
    #print "*** External Header ***"
    sd.process_external_headers ()
    #print_container (sd.reel_headers.external_header)
    #i = 1
    #for c in sd.reel_headers.external_header_shot :
        #print i; i += 1
        #print_container (c)
    #n = 1
    
def trace_headers (sd) :
    n = 1
    print "*** Trace Header ***", n
    
    sd.process_trace_headers ()
    print_container (sd.trace_headers.trace_header)
    i = 1
    for c in sd.trace_headers.trace_header_N :
        print i; i += 1
        print_container (c)
        
    trace = sd.read_trace (sd.samples)
    #for s in trace :
        #print s
    #n += 1
    while True :
        if sd.isEOF () :
            break
        print "*** Trace Header ***", n
        sd.process_trace_headers ()
        print_container (sd.trace_headers.trace_header)
        i = 1
        for c in sd.trace_headers.trace_header_N :
            print i; i += 1
            print_container (c)
        
        n += 1    
        trace = sd.read_trace (sd.samples)
        #for s in trace :
            #print s    
            
    print "There were {0} traces.".format (n)
    
if __name__ == '__main__' :
    global RH, TH
    TH = []
    outpath = sys.argv[2]
    if not os.path.exists (outpath) :
        os.makedirs (outpath)
    with open (sys.argv[1]) as fh :
        while True :
            line = fh.readline ()
            if not line : break
            filename = line.strip ()
            if not os.path.exists (filename) :
                sys.stderr.write ("Warning: can't find: {0}\n".format (filename))
                continue
            RH = SegdReader.ReelHeaders () 
            try :
                sd = SegdReader.Reader (infile=filename)
            except :
                sys.stderr.write ("Failed to properly read {0}.\n".format (filename))
                sys.exit ()
            
            general_headers (sd)
            channel_set_descriptors (sd)
            extended_headers (sd)
            external_header (sd)
            
            #print "{0} bytes read.".format (sd.bytes_read)
            line_number = sd.reel_headers.extended_header_3['line_number']
            receiver_point = sd.reel_headers.extended_header_3['receiver_point']
            version = sd.reel_headers.general_header_block_2['file_version_number']
            outfile = "R{0}_{1}.0.0.rg{2}".format (line_number, receiver_point, 16)
            linkname = os.path.join (outpath, outfile)
            i = 0
            while os.path.exists (linkname) :
                i += 1
                outfile = "R{0}_{1}.0.{3}.rg{2}".format (line_number, receiver_point, 16, i)
                linkname = os.path.join (outpath, outfile)
                
            try :
                print filename, '->', linkname
                os.link (filename, linkname)
            except Exception as e :
                print e.message