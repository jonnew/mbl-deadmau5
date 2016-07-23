from nose.tools import *
from acat.acatsm import AcatSM
from acat.maze import Maze, RwdSite
from acat.tracker import Tracker
import time

def test_AcatSM():

    #/home/jon/public/acat/audio-cues/
    #/home/jon/public/acat/audio-cues/    
    fail_noise = 'white_-6dBFS_3s.wav'

    rwd_sites = [ 
        RwdSite(name='R0', wavfile='sweep_2000Hz_200Hz_-6dBFS_1s.wav'),         
        RwdSite(name='R1', wavfile='sweep_200Hz_2000Hz_-6dBFS_1s.wav'),         
    ]

    maze = Maze(rwd_sites, fail_noise)
    sm = AcatSM(maze)
    #sm.graph.draw('ACAT-SM.png', prog='dot')

    # Cannot enter reward location before starting trial
    sm.enter_rwd_location()
    assert_equal(sm.state, 'initialized')

    # Upon entering start port, trial is started
    sm.enter_start_port()
    assert_equal(sm.state, 'trial_started')

    # After starting trial, it cannot be restarted
    sm.enter_start_port()
    assert_equal(sm.state, 'trial_started')

    # If animal enters correct reward site, reward is delivered
    pos = {'pos_xy': [1.0, 1.0], 'reg': sm.maze.rwd_sites[sm.maze.cued_rwd_site].name}
    sm.enter_rwd_location(position=pos)
    assert_equal(sm.state, 'rwd_delivered')

    # After reward is delivered, automatic transition to initialized
    sm.start_next_trial()
    assert_equal(sm.state, 'initialized')

    # Upon entering start port, trial is started
    sm.enter_start_port()
    assert_equal(sm.state, 'trial_started')

    # If animal enters correct reward site, reward is delivered
    pos = {'pos_xy': [1.0, 1.0], 'reg': 'Wrong'}
    sm.enter_rwd_location(position=pos)
    assert_equal(sm.state, 'failure')

    # After failure automatic transition to initialized
    sm.start_next_trial()
    assert_equal(sm.state, 'initialized')

    # TODO:
    ## Upon entering start port, trial is started
    #sm.enter_start_port()
    #assert_equal(sm.state, 'trial_started')

    ## If the animal waits too long, there is a decision timeout to failure
    #dt = sm.decision_duration_sec
    #time.sleep(dt + 10)
    #assert_equal(sm.state, 'failure')
