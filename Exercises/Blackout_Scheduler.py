#! /usr/bin/env python

import Blackout_Scheduler_Config as Cfg
import logging.handlers
import re
import datetime
import requests
import json
from jinja2 import Environment, PackageLoader, select_autoescape
import sys

from flask import Flask, render_template, request
from lxml import etree
from datetime import datetime as dt, timedelta
from copy import deepcopy


app = Flask(__name__)
media = ''
programs = []
logger = logging.getLogger('BlackoutLogger')
logger.setLevel(Cfg.log_level)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(funcName)s] %(message)s')
handler = logging.handlers.TimedRotatingFileHandler(Cfg.log_filename, when=Cfg.log_when, interval=1,
                                                    backupCount=Cfg.log_backup_Count)
handler.setFormatter(formatter)
logger.addHandler(handler)

if Cfg.console_logging:
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)
else:
    sys.stdout = sys.stderr = open(Cfg.log_filename, 'wt')


class Program:
    def __init__(self, programid, effective, desc=""):
        self.id = programid
        self.effective = effective
        self.desc = desc


def get_media_from_cadent(providerid, networkid):
    global programs
    global media
    try:
        programs = []
        cadent_url = ''
        if providerid == 'DISNEY':
            cadent_url = Cfg.cadent_url_disney + '?role=Media&limit=100&updatedAfter>=' + \
                         dt.utcnow().strftime('%Y-%m-%d')
        elif providerid == 'TURNER':
            cadent_url = Cfg.cadent_url_turner + '?role=Media&limit=1000&updatedAfter>=' + \
                         dt.utcnow().strftime('%Y-%m-%d')
        elif providerid == 'FOX':
            cadent_url = Cfg.cadent_url_fox + networkid

        logger.debug(cadent_url)
        response = requests.get(url=cadent_url, verify=False)
        res = response.text.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '')
        logger.debug(response.status_code)
        tree = etree.ElementTree(etree.fromstring(res))
        nsmap = {'ns': 'http://www.scte.org/schemas/224'}
        root = tree.getroot()
        if providerid == 'FOX':
            medias = root.findall("ns:MediaPoint", nsmap)
        else:
            medias = root.findall("ns:Media", nsmap)
        if len(medias) > 0:
            for med in medias:
                try:
                    expiretime = dt.strptime(med.attrib['expires'], '%Y-%m-%dT%H:%M:%SZ')
                    if providerid == 'FOX':
                        if med.attrib['id'].find('/start') >= 0:
                            if expiretime > dt.utcnow():
                                programs.append(
                                    Program(med.attrib['id'][:-6], med.attrib['effective'], med.attrib['description']))

                    elif len(re.findall('\\b' + networkid + '\\b', med.attrib['id'])) > 0 and expiretime >= dt.utcnow():
                        if providerid == 'DISNEY':
                            programs.insert(0, Program(med.attrib['id'].replace('/disney.com/'+networkid+'/program/',
                                                                                ''), med.attrib['effective']))
                        elif providerid == 'TURNER':
                            programs.insert(0,
                                            Program(med.attrib['id'].replace('turner.com/'+networkid+'/program/', ''),
                                                    med.attrib['description'] + '-' + med.attrib['effective'] + '-'
                                                    + med.attrib['expires']))
                except Exception as looperr:
                    logger.debug(looperr)
                    continue
        return etree.tostring(root)
    except Exception as getMedErr:
        raise getMedErr


def generate_media_for_create(progid, botype, network):
    global media
    try:
        tree = etree.ElementTree(etree.fromstring(media))
        nsmap = {'ns': 'http://www.scte.org/schemas/224'}
        root = tree.getroot()
        mediapoints = root.findall("ns:MediaPoint", nsmap)
        if len(mediapoints) > 0:
            for mediapoint in mediapoints:
                if mediapoint.attrib['id'] == (progid + '/start'):
                    src = mediapoint.attrib['source']
                    applyelem = etree.Element('Apply')
                    appolicy = etree.Element('Policy')
                    # netapplyelem = etree.Element('Apply')
                    # netapppolicy = etree.Element('Policy')

                    rmlist = mediapoint.findall("ns:Remove", nsmap)
                    aplist = mediapoint.findall("ns:Apply", nsmap)
                    if rmlist is not None:
                        for rm in rmlist:
                            mediapoint.remove(rm)
                    if aplist is not None:
                        for ap in aplist:
                            mediapoint.remove(ap)
                    if botype == "encoder":
                        appolicy.set("{http://www.w3.org/1999/xlink}href", "fox/policy/any.all/blackout")
                        applyelem.append(appolicy)
                        mediapoint.insert(1, applyelem)
                    elif botype == "device-phone" or botype == "device-tablet" or botype == "device-both":
                        # netapppolicy.set("{http://www.w3.org/1999/xlink}href", "fox/policy/" + network + ".all/" + src)
                        # netapplyelem.append(netapppolicy)
                        if botype == "device-phone":
                            appolicy.set("{http://www.w3.org/1999/xlink}href", "fox/policy/" + network + ".noPhone/" +
                                         src)
                        elif botype == "device-tablet":
                            appolicy.set("{http://www.w3.org/1999/xlink}href", "fox/policy/" + network + ".noTablet/" +
                                         src)
                        elif botype == "device-both":
                            appolicy.set("{http://www.w3.org/1999/xlink}href", "fox/policy/" + network +
                                         ".noPhone.noTablet/" + src)
                        applyelem.append(appolicy)
                        # mediapoint.insert(1, netapplyelem)
                        mediapoint.insert(1, applyelem)
                if mediapoint.attrib['id'] == (progid + '/end'):
                    src = mediapoint.attrib['source']
                    remove = etree.Element('Remove')
                    rmpolicy = etree.Element('Policy')
                    # netremove = etree.Element('Remove')
                    # netrmpolicy = etree.Element('Policy')
                    rmlist = mediapoint.findall("ns:Remove", nsmap)
                    aplist = mediapoint.findall("ns:Apply", nsmap)
                    if rmlist is not None:
                        for rm in rmlist:
                            mediapoint.remove(rm)
                    if aplist is not None:
                        for ap in aplist:
                            mediapoint.remove(ap)
                    if botype == "encoder":
                        rmpolicy.set("{http://www.w3.org/1999/xlink}href", "fox/policy/any.all/blackout")
                        remove.append(rmpolicy)
                        mediapoint.insert(1, remove)
                    elif botype == "device-phone" or botype == "device-tablet" or botype == "device-both":
                        # netrmpolicy.set("{http://www.w3.org/1999/xlink}href", "fox/policy/" + network + ".all/" + src)
                        # netremove.append(netrmpolicy)
                        if botype == "device-phone":
                            rmpolicy.set("{http://www.w3.org/1999/xlink}href", "fox/policy/" + network + ".noPhone/" +
                                         src)
                        elif botype == "device-tablet":
                            rmpolicy.set("{http://www.w3.org/1999/xlink}href", "fox/policy/" + network + ".noTablet/" +
                                         src)
                        elif botype == "device-both":
                            rmpolicy.set("{http://www.w3.org/1999/xlink}href", "fox/policy/" + network +
                                         ".noPhone.noTablet/" + src)
                        remove.append(rmpolicy)
                        mediapoint.insert(1, remove)
                        # mediapoint.insert(2, netremove)
        media_to_cadent = etree.tostring(root)
        parser = etree.XMLParser(remove_blank_text=True)
        xml = etree.fromstring(media_to_cadent, parser=parser)
        media_to_cadent = etree.tostring(xml, pretty_print=True)
        media = media_to_cadent
    except Exception as createerr:
        raise createerr


def generate_media_for_remove(progid, network):
    global media
    try:
        tree = etree.ElementTree(etree.fromstring(media))
        nsmap = {'ns': 'http://www.scte.org/schemas/224'}
        root = tree.getroot()
        mediapoints = root.findall("ns:MediaPoint", nsmap)
        if len(mediapoints) > 0:
            for mediapoint in mediapoints:
                if mediapoint.attrib['id'] == (progid + '/start'):
                    src = mediapoint.attrib['source']
                    applyelem = etree.Element('Apply')
                    appolicy = etree.Element('Policy')
                    appolicy.set("{http://www.w3.org/1999/xlink}href", "fox/policy/" + network + ".all/" + src)
                    applyelem.append(appolicy)
                    rmlist = mediapoint.findall("ns:Remove", nsmap)
                    aplist = mediapoint.findall("ns:Apply", nsmap)
                    if rmlist is not None:
                        for rm in rmlist:
                            mediapoint.remove(rm)
                    if aplist is not None:
                        for ap in aplist:
                            mediapoint.remove(ap)
                    mediapoint.insert(1, applyelem)
                elif mediapoint.attrib['id'] == (progid + '/end'):
                    src = mediapoint.attrib['source']
                    remove = etree.Element('Remove')
                    rmpolicy = etree.Element('Policy')
                    rmpolicy.set("{http://www.w3.org/1999/xlink}href", "fox/policy/" + network + ".all/" + src)
                    remove.append(rmpolicy)
                    rmlist = mediapoint.findall("ns:Remove", nsmap)
                    aplist = mediapoint.findall("ns:Apply", nsmap)
                    if rmlist is not None:
                        for rm in rmlist:
                            mediapoint.remove(rm)
                    if aplist is not None:
                        for ap in aplist:
                            mediapoint.remove(ap)
                    mediapoint.insert(1, remove)

        media_to_cadent = etree.tostring(root)
        parser = etree.XMLParser(remove_blank_text=True)
        xml = etree.fromstring(media_to_cadent, parser=parser)
        media_to_cadent = etree.tostring(xml, pretty_print=True)
        media = media_to_cadent
    except Exception as removeerr:
        raise removeerr


def remove_mediapoint(progid):
    global media
    try:
        tree = etree.ElementTree(etree.fromstring(media))
        nsmap = {'ns': 'http://www.scte.org/schemas/224'}
        root = tree.getroot()
        mediapoints = root.findall("ns:MediaPoint", nsmap)
        if len(mediapoints) > 0:
            for mediapoint in mediapoints:
                if mediapoint.attrib['id'] == (progid + '/start') or mediapoint.attrib['id'] == (progid + '/end'):
                    root.remove(mediapoint)
        media_to_cadent = etree.tostring(root)
        parser = etree.XMLParser(remove_blank_text=True)
        xml = etree.fromstring(media_to_cadent, parser=parser)
        media_to_cadent = etree.tostring(xml, pretty_print=True)
        media = media_to_cadent
    except Exception as removeerr:
        raise removeerr


def find_media_from_entiremedia(networkid, mediaid):
    try:
        tree = etree.ElementTree(etree.fromstring(media))
        nsmap = {'ns': 'http://www.scte.org/schemas/224'}
        root = tree.getroot()
        medias = root.findall("ns:Media", nsmap)
        if len(medias) > 0:
            for med in medias:
                if med.attrib['id'].find(networkid + '/program/' + mediaid) > 0:
                    return etree.tostring(med)
    except Exception as findMedErr:
        raise findMedErr


def get_update_media(networkid, mediaid):
    try:

        mediastr = find_media_from_entiremedia(networkid, mediaid)
        tree = etree.ElementTree(etree.fromstring(mediastr))
        root = tree.getroot()
        mediaxml = etree.tostring(root)
        parser = etree.XMLParser(remove_blank_text=True)
        mediaxml = etree.fromstring(mediaxml, parser=parser)
        mediaxml = etree.tostring(mediaxml, pretty_print=True).decode(encoding='utf-8')
        return mediaxml
    except Exception as updMedErr:
        raise updMedErr


def apply_action(mediaid, network, mediastr, medaction):
    try:
        media_to_cadent = ''
        if medaction == 'ApplyGeoBO':
            media_to_cadent = apply_geo_bo(mediaid, network, mediastr)
        elif medaction == 'ApplyWebBO':
            media_to_cadent = apply_web_bo(mediaid, network, mediastr)
        elif medaction == "RemoveGeoBO":
            media_to_cadent = remove_geo_bo(mediastr)
        elif medaction == "RemoveWebBO":
            media_to_cadent = remove_web_bo(mediastr, mediaid)
        elif medaction == "AddGeoBOOvrdMP":
            media_to_cadent = add_bo_ovrd_mp("geo", mediastr)
        elif medaction == "AddGeoBOLiftOvrdMP":
            media_to_cadent = add_bo_ovrd_mp("geo_lift", mediastr)
        elif medaction == "RemoveGeoBOOvrdMP":
            media_to_cadent = rm_bo_ovrd_mp("geo", mediastr)
        elif medaction == "RemoveGeoBOLiftOvrdMP":
            media_to_cadent = rm_bo_ovrd_mp("geo_lift", mediastr)
        elif medaction == "AddWebBOOvrdMP":
            media_to_cadent = add_bo_ovrd_mp("web", mediastr)
        elif medaction == "RemoveWebBOOvrdMP":
            media_to_cadent = rm_bo_ovrd_mp("web", mediastr)
        elif medaction == "AddWebBOLiftOvrdMP":
            media_to_cadent = add_bo_ovrd_mp("web_lift", mediastr)
        elif medaction == "RemoveWebBOLiftOvrdMP":
            media_to_cadent = rm_bo_ovrd_mp("web_lift", mediastr)

        parser = etree.XMLParser(remove_blank_text=True)
        xml = etree.fromstring(media_to_cadent, parser=parser)
        media_to_cadent = etree.tostring(xml, pretty_print=True).decode(encoding='utf-8')
        return media_to_cadent

    except Exception as appactionerr:
        raise appactionerr


def add_bo_ovrd_mp(bo_type, mediastr):
    """
    method to add either a geo black out override media point or add a geo blackout lift override media point to the
    mediastr
    :param bo_type: the type of blackout override media point you want to implement. 'geo' and 'geo_lift' are supported
    :param mediastr: the string representation of 224 data
    :return: string representation of 224 data with blackout of type bo_type added
    """

    try:
        # ensure we don't add more than one mediapoint
        mediastr = rm_bo_ovrd_mp(bo_type, mediastr)

        tree = etree.ElementTree(etree.fromstring(mediastr))
        nsmap = {'ns': 'http://www.scte.org/schemas/224'}
        root = tree.getroot()

        mediapoints = root.findall("ns:MediaPoint", nsmap)
        new_mediapoint = None

        for mediapoint in mediapoints:
            if 'geo_lift' == bo_type or 'web_lift' == bo_type:
                if 'end' in mediapoint.attrib['id']:
                    new_mediapoint = deepcopy(mediapoint)
                else:
                    continue

            elif 'geo' == bo_type or 'web' == bo_type:
                if 'start' in mediapoint.attrib['id']:
                    new_mediapoint = deepcopy(mediapoint)
                else:
                    continue

            # remove expectedDuration attribute in geo_override media point
            if 'expectedDuration' in new_mediapoint.attrib.keys():
                del (new_mediapoint.attrib['expectedDuration'])

            # loop through child of media point to find Apply/MatchSignal tag
            for child_tag in new_mediapoint.getchildren():
                if 'Apply' in child_tag.tag or 'Remove' in child_tag.tag:

                    # remove all the apply tag attributes
                    for key in child_tag.attrib:
                        del (child_tag.attrib[key])

                    # get child Policy tag and append 'blackout' to the end or 'default' if web blackout
                    for inner_tag in child_tag.getchildren():
                        for item in inner_tag.attrib.items():
                            if 'href' in item[0]:
                                if bo_type == 'web' or bo_type == 'web_lift':
                                    '''
                                    in the case of a web blackout replace
                                    turner.com/TNTE/policy/952051395 with turner.com/TNTE/policy/default
                                    '''
                                    inner_tag.set(item[0], '/'.join(item[1].split('/')[:-1]) + '/default')
                                else:
                                    if 'blackout' in item[1]:
                                        new_mediapoint.remove(child_tag)
                                    else:
                                        inner_tag.set(item[0], '/'.join(item[1].split('/')[:-1]) + '/' + str(Cfg.geo_blackout_policy_id) + "/blackout")

                # change segmenttypeid and deliveryrestrictions of apply tag in match signal depending on bo_type
                elif 'MatchSignal' in child_tag.tag:
                    # remove signalTolerance
                    del(child_tag.attrib['signalTolerance'])
                    for inner_tag in child_tag.getchildren():
                        if 'Assert' in inner_tag.tag:
                            if 'geo' == bo_type:
                                inner_tag.text = "/SpliceInfoSection/SegmentationDescriptor[@segmentationTypeId = 24]/DeliveryRestrictions[@noRegionalBlackoutFlag = 'false']"

                            elif 'geo_lift' == bo_type:
                                inner_tag.text = "/SpliceInfoSection/SegmentationDescriptor[@segmentationTypeId = 24]/DeliveryRestrictions[@noRegionalBlackoutFlag = 'true']"

                            elif 'web' == bo_type:
                                inner_tag.text = "/SpliceInfoSection/SegmentationDescriptor[@segmentationTypeId = 24]/DeliveryRestrictions[@webDeliveryAllowedFlag = 'false']"

                            elif 'web_lift' == bo_type:
                                inner_tag.text = "/SpliceInfoSection/SegmentationDescriptor[@segmentationTypeId = 24]/DeliveryRestrictions[@webDeliveryAllowedFlag = 'true']"

                else:
                    new_mediapoint.remove(child_tag)

            # decrement or increment effective, matchtime and expires attributes of mediapoint depending on bo_type
            if 'lift' in bo_type:
                # lift means we decrement by 15 minutes
                new_mediapoint.set('effective', add_remove_time(mediapoint.attrib['effective'], add=False))
                new_mediapoint.set('matchTime', add_remove_time(mediapoint.attrib['matchTime'], add=False))
                new_mediapoint.set('expires', add_remove_time(mediapoint.attrib['expires'], add=False))

            else:
                # non lifts mean we increment by 15 minutes
                new_mediapoint.set('effective', add_remove_time(mediapoint.attrib['effective'], add=True))
                new_mediapoint.set('matchTime', add_remove_time(mediapoint.attrib['matchTime'], add=True))
                new_mediapoint.set('expires', add_remove_time(mediapoint.attrib['expires'], add=True))

            # change id field of mediapoint based on bo_type, per cadent 22.01 fix this is how the id's should look
            if 'geo' == bo_type or 'web' == bo_type:
                # change id="/program/955462273/start to id="/program/955462273/blackout
                new_mediapoint.set('id', mediapoint.attrib['id'].replace('start',  'blackout'))

            if 'geo_lift' == bo_type or 'web_lift' == bo_type:
                # change id="/program/955462273/start to id="/program/955462273/blackoutlift
                new_mediapoint.set('id', mediapoint.attrib['id'].replace('end',  'blackoutlift'))


            insert_ovrd_media(bo_type, root, new_mediapoint)
            return etree.tostring(root)

    except Exception as e:
        raise e


def insert_ovrd_media(bo_type, root, new_mediapoint):
    """
    method to insert an ovrd media point into 224 data
    :param bo_type: string, the type of bo override you are trying to insert into the mediastr
    :param root: list, of elements in the 224 data you are trying to insert a blackout of bo_type into
    :param new_mediapoint: lxml.etree._Element object, the media point object we are trying to insert into the root list
    :return: None
    """

    for el in root:

        if "MediaPoint" not in el.tag:
            continue

        if el.attrib['id'].endswith('start'):
            continue

        if el.attrib['id'].split('/')[-1] == 'webblackoutlift' and bo_type == 'web':
            el.addprevious(new_mediapoint)
            return

        if el.attrib['id'].split('/')[-1] == 'webblackout' and bo_type == 'web_lift':
            el.addnext(new_mediapoint)
            return

        if el.attrib['id'].split('/')[-1] == 'blackoutlift' and bo_type == 'geo':
            el.addprevious(new_mediapoint)
            return

        if el.attrib['id'].split('/')[-1] == 'blackout' and bo_type == 'geo_lift':
            el.addnext(new_mediapoint)
            return

        elif el.attrib['id'].split('/')[-1] == 'end':
            el.addprevious(new_mediapoint)
            return


def rm_bo_ovrd_mp(bo_type, mediastr):
    """
    method to remove either a geo black out override media point or add a geo blackout lift override media point
    from the mediastr
    :param bo_type: the type of blackout override media point you want to remove. 'geo' and 'geo_lift' are supported
    :param mediastr: the string representation of 224 data
    :return: string representation of 224 data with blackout of type bo_type removed
    """

    try:
        tree = etree.ElementTree(etree.fromstring(mediastr))
        nsmap = {'ns': 'http://www.scte.org/schemas/224'}
        root = tree.getroot()
        mp_to_remove = list()

        mediapoints = root.findall("ns:MediaPoint", nsmap)

        # loop through and look for specific kind of bo_type to remove
        for mediapoint in mediapoints:

            if bo_type == 'web' and mediapoint.attrib['id'].split('/')[-1] == 'blackout':
                mp_to_remove.append(mediapoint)

            if bo_type == 'web_lift' and mediapoint.attrib['id'].split('/')[-1] == 'blackoutlift':
                mp_to_remove.append(mediapoint)

            if bo_type == 'geo' and mediapoint.attrib['id'].split('/')[-1] == 'blackout':
                mp_to_remove.append(mediapoint)

            if bo_type == 'geo_lift' and mediapoint.attrib['id'].split('/')[-1] == 'blackoutlift':
                mp_to_remove.append(mediapoint)

        for mp in mp_to_remove:
            root.remove(mp)

        return etree.tostring(root)

    except Exception as e:
        raise e


def add_remove_time(time, add=True):
    """
    method to take the string representation of UTC time as seen in the effective/matchtime,expires field of MediaPoint
    tags in 224 data, and either adds 15 minutes or removes 15 minutes and returns the new time as a string that is
    formatted the same as the input: "%Y-%m-%dT%H:%M:%SZ"

    This is a helper method for the actions:
        - Add Geo Blackout Override Media point
        - Add Geo Blackout Lift Override Media point

    :param time: the string representation of UTC time in form "%Y-%m-%dT%H:%M:%SZ"
    :param add: bool, should we add (True) or remove (False) 15 minutes. True by default
    :return: string representation of UTC time with either +15 minutes or -15 minutes depending on parameter "add"
    string time is returned in the format "%Y-%m-%dT%H:%M:%SZ"
    """
    t = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")

    if add:
        t += datetime.timedelta(minutes=15)
    else:
        t -= datetime.timedelta(minutes=15)

    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def copy_media(mediastr, mediaid):
    """
    method to take in a string containing 224 data and "copy" it, which means appending _1 to the mediaid,
    returning 224 data with _1 appended to the mediaid in the id field of the Media tag and both MediaPoints
    :param mediastr: string representation of 224 data
    :param mediaid: string representation of the 9 digit mediaid for the program we are removing the web blackout for
    :return: string
    """

    try:
        tree = etree.ElementTree(etree.fromstring(mediastr))
        nsmap = {'ns': 'http://www.scte.org/schemas/224'}
        root = tree.getroot()
        root.set('id', root.attrib['id'] + '_1')

        mediapoints = root.findall("ns:MediaPoint", nsmap)
        if len(mediapoints) > 0:

            # turn id="/program/956962599/start into id="/program/956962599_1/start
            # turn id="/program/956962599/end into id="/program/956962599_1/end
            for mediapoint in mediapoints:
                mediapoint_id = mediapoint.attrib['id'].split('/')
                for i in range(0, len(mediapoint_id)):
                    if mediapoint_id[i] == mediaid:
                        mediapoint_id[i] = mediapoint_id[i] + '_1'
                        break

                mediapoint.set('id', '/'.join(mediapoint_id))

        return etree.tostring(root)

    except Exception as e:
        raise e


def apply_geo_bo(mediaid, network, mediastr):
    try:
        tree = etree.ElementTree(etree.fromstring(mediastr))
        nsmap = {'ns': 'http://www.scte.org/schemas/224'}
        root = tree.getroot()
        mediapoints = root.findall("ns:MediaPoint", nsmap)
        if len(mediapoints) > 0:
            for mediapoint in mediapoints:
                if mediapoint.attrib['id'] == ('/program/' + mediaid + '/start'):
                    applyelem = etree.Element('Apply')
                    appolicy = etree.Element('Policy')
                    aplist = mediapoint.findall("ns:Apply", nsmap)
                    if aplist is not None and len(aplist) > 1:
                        mediapoint.remove(aplist[1])
                    appolicy.set("{http://www.w3.org/1999/xlink}href", "turner.com/" + network +
                                 "/policy/" + str(Cfg.geo_blackout_policy_id) + "/blackout")
                    applyelem.append(appolicy)
                    mediapoint.insert(3, applyelem)
                if mediapoint.attrib['id'] == ('/program/' + mediaid + '/end'):
                    remove = etree.Element('Remove')
                    rmpolicy = etree.Element('Policy')
                    rmlist = mediapoint.findall("ns:Remove", nsmap)
                    if rmlist is not None and len(rmlist) > 1:
                        mediapoint.remove(rmlist[0])
                    rmpolicy.set("{http://www.w3.org/1999/xlink}href", "turner.com/" + network +
                                 "/policy/" + str(Cfg.geo_blackout_policy_id) + "/blackout")
                    remove.append(rmpolicy)
                    mediapoint.insert(1, remove)

        media_to_cadent = etree.tostring(root)

        return media_to_cadent
    except Exception as applygeoboeerr:
        raise applygeoboeerr


def apply_web_bo(mediaid, network, mediastr):
    try:
        tree = etree.ElementTree(etree.fromstring(mediastr))
        nsmap = {'ns': 'http://www.scte.org/schemas/224'}
        root = tree.getroot()
        apply_attributes = dict()
        mediapoints = root.findall("ns:MediaPoint", nsmap)
        if len(mediapoints) > 0:
            for mediapoint in mediapoints:
                if mediapoint.attrib['id'] == ('/program/' + mediaid + '/start'):
                    applyelem = etree.Element('Apply')
                    appolicy = etree.Element('Policy')
                    aplist = mediapoint.findall("ns:Apply", nsmap)
                    if aplist is not None and len(aplist) > 0:
                        mediapoint.remove(aplist[0])

                        # save the duration and priority attribute of the apply tag we're removing
                        apply_attributes = aplist[0].attrib

                    appolicy.set("{http://www.w3.org/1999/xlink}href", "turner.com/" + network + "/policy/default")

                    # make sure we're adding the duration and priority attributes of the previous apply tag
                    for item in apply_attributes.items():
                        applyelem.set(item[0], item[1])

                    applyelem.append(appolicy)
                    mediapoint.insert(2, applyelem)
                if mediapoint.attrib['id'] == ('/program/' + mediaid + '/end'):
                    remove = etree.Element('Remove')
                    rmpolicy = etree.Element('Policy')
                    rmlist = mediapoint.findall("ns:Remove", nsmap)
                    if rmlist is not None and len(rmlist) > 0:
                        mediapoint.remove(rmlist[0])
                    rmpolicy.set("{http://www.w3.org/1999/xlink}href", "turner.com/" + network + "/policy/default")
                    remove.append(rmpolicy)
                    mediapoint.insert(1, remove)

        media_to_cadent = etree.tostring(root)

        return media_to_cadent
    except Exception as applywebboeerr:
        raise applywebboeerr


def remove_web_bo(mediastr, mediaid):
    """
    method to take in a string containing 224 data and remove the web blackout policies from it,
    returning 224 data with no web blackout policies
    :param mediastr: string representation of 224 data containing a web blackout
    :param mediaid: string representation of the 9 digit mediaid for the program we are removing the web blackout for
    :return: string
    """

    try:
        tree = etree.ElementTree(etree.fromstring(mediastr))
        nsmap = {'ns': 'http://www.scte.org/schemas/224'}
        root = tree.getroot()
        mediapoints = root.findall("ns:MediaPoint", nsmap)
        if len(mediapoints) > 0:

            for mediapoint in mediapoints:
                if 'start' in mediapoint.attrib['id'] or 'end' in mediapoint.attrib['id']:
                    '''
                    change web blackout by changing apply policy: 
                    turner.com/CTN/policy/default -> turner.com/CTN/policy/{mediaid}
                    '''
                    for apply_el in mediapoint.findall("ns:Apply", nsmap):
                        contains_blackout_policy(apply_el, 'web', mediaid)

                    '''
                    change web blackout by changing remove policy:
                    turner.com/CTN/policy/default -> turner.com/CTN/policy/{mediaid}
                    '''
                    for remove_el in mediapoint.findall("ns:Remove", nsmap):
                        contains_blackout_policy(remove_el, 'web', mediaid)

        return etree.tostring(root)

    except Exception as e:
        raise e


def remove_geo_bo(mediastr):
    """
    method to take in a string containing 224 data and remove the geo blackout policies from it,
    returning 224 data with no geo blackout policies
    :param mediastr: string representation of 224 data containing a geo blackout
    :return: string
    """

    try:
        tree = etree.ElementTree(etree.fromstring(mediastr))
        nsmap = {'ns': 'http://www.scte.org/schemas/224'}
        root = tree.getroot()
        mediapoints = root.findall("ns:MediaPoint", nsmap)
        if len(mediapoints) > 0:

            # remove blackout policies contained in <Apply> tags
            for mediapoint in mediapoints:
                # don't mess with bo lift + bo lift overrides
                if 'start' in mediapoint.attrib['id'] or 'end' in mediapoint.attrib['id']:
                    for apply_el in mediapoint.findall("ns:Apply", nsmap):
                        if contains_blackout_policy(apply_el, 'geo'):
                            mediapoint.remove(apply_el)

                    # remove blackout policies contained in <Remove> tags
                    for remove_el in mediapoint.findall("ns:Remove", nsmap):
                        if contains_blackout_policy(remove_el, 'geo'):
                            mediapoint.remove(remove_el)

        return etree.tostring(root)

    except Exception as e:
        raise e


def contains_blackout_policy(apply_remove_tag, bo_type, mediaid=None):
    """
    WEIRD BEHAVIOR, FOR WEB IT ACTUALLY MODIFIES POLICY. FIX THIS
    given an Apply or Remove tag, determine if the child policy tag is a blackout
    :param apply_remove_tag: lxml.etree_Element object representing the Apply or Remove tag in question
    :param bo_type: the type of blackout you want to remove
    :param mediaid: if doing a web blackout, the mediaid is used to replace the word 'default' in the blackout policy
    :return: bool
    """

    for policy in apply_remove_tag.getchildren():
        for item in policy.attrib.items():
            if 'href' in item[0]:
                if bo_type == 'geo':
                    if '/blackout' in item[1]:
                        return True
                if bo_type == 'web':
                    if '/default' in item[1]:
                        policy.set(item[0], item[1].replace('default', mediaid))
                        return True

    return False


def post_media_to_cadent(providerid, network, mediaid, mediastr, action):
    try:
        response = ''
        cadent_url = ''
        strresult = '<Results xmlns="http://www.scte.org/schemas/224" xmlns:cadent="urn:cadent:224" ' \
                    'xmlns:ns5="urn:scte:224:metadata" xmlns:audience="urn:scte:224:audience" ' \
                    'xmlns:action="urn:scte:224:action" xmlns:xlink="http://www.w3.org/1999/xlink" ' \
                    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        headers = {
            'Content-Type': 'application/xml'}
        if providerid == 'DISNEY':
            if action in ('update', 'delete'):
                cadent_url = Cfg.cadent_url_disney + '/disney.com/' + network + '/program/' + mediaid
        elif providerid == 'TURNER':
            if action == 'update' or action == 'CopyUpdate':
                mediastr = strresult + mediastr + '</Results>'
                cadent_url = Cfg.cadent_url_turner
            elif action == 'delete':
                cadent_url = Cfg.cadent_url_turner + '/turner.com/' + network + '/program/' + mediaid
        elif providerid == 'FOX':
            cadent_url = Cfg.cadent_url_fox + network

        logger.debug(cadent_url)
        logger.debug(mediastr)

        if action == 'update' or action == 'CopyUpdate':
            response = requests.put(url=cadent_url, headers=headers, data=mediastr, verify=False)
        elif action == 'delete':
            response = requests.delete(url=cadent_url, verify=False)

        logger.debug(str(response.status_code) + "-" + response.text)

        return str(response.status_code) + "-" + response.text
    except Exception as posterr:
        raise posterr


def determine_dropdown_behavior(mediastr):
    """
     method to generate two booleans that will determine what actions are shown in the
     action drop down for turner blackouts in the blackout scheduler ui

    :param mediastr: str the string representation of the 224 the user is modifying
    :return: a tuple containing two booleans, (show_geo_bo, show_web_bo)
    """

    try:
        tree = etree.ElementTree(etree.fromstring(mediastr))
        nsmap = {'ns': 'http://www.scte.org/schemas/224'}
        root = tree.getroot()
        mediapoints = root.findall("ns:MediaPoint", nsmap)

        for mediapoint in mediapoints:
            for mp_child_tag in mediapoint.getchildren():
                if "Apply" in mp_child_tag.tag or "Remove" in mp_child_tag.tag:
                    for policy in mp_child_tag.getchildren():
                        for item in policy.attrib.items():
                            if 'href' in item[0]:
                                if '/blackout' in item[1]:
                                    return True, False
                                if '/default' in item[1]:
                                    return False, True

        return True, True

    except Exception as determinedropdownbehaviorErr:
        raise determinedropdownbehaviorErr

def parse_mediaid(updmedia):
    '''
    Grab the mediaid from the 224 (incase user has manually changed the id) so creation/updates and deletes will work
    :param updmedia: str the 224 data from the form
    :return: str the mediaid parsed from the 224
    '''
    tree = etree.ElementTree(etree.fromstring(updmedia))
    root = tree.getroot()

    return root.attrib['id'].split('/')[-1]


@app.route("/main", methods=('get', 'post'))
def main():
    '''
    for turner I need to fix the following
    parsing mediaID when user hits submit to apply an action (ran into situation where delete wasn't working with mediaID_1)
    '''
    provider = ''
    network = ''
    updmedia = ''
    mediaid = ''
    cad_res = ''
    medaction = ''

    global media
    global programs

    # variables to control what's being shown in list of drop down actions for Turner
    show_geo_bo = True
    show_web_bo = True

    try:
        if request.args.get('action') == "getnetworks":
            provider = request.form.get("provider")
            programs = []
        elif request.args.get('action') == "getmedia":
            provider = request.form.get("provider")
            network = request.form.get("network")
            if provider == '' or network == "":
                programs = []
            else:
                media = get_media_from_cadent(provider, network)
                if provider == 'FOX':
                    updmedia = media
                else:
                    updmedia = ''

        elif request.args.get('action') == "getmediaforprogram":
            provider = request.form.get("provider")
            network = request.form.get("network")
            mediaid = request.form.get("program")
            if provider == "FOX":
                updmedia = media
            else:
                updmedia = get_update_media(network, mediaid)

        elif request.args.get('action') == "ApplyAction":
            provider = request.form.get("provider")
            network = request.form.get("network")
            mediaid = request.form.get("program")
            medaction = request.form.get("medAction")
            updmedia = request.form.get("updMediaxml")
            updmedia = apply_action(mediaid, network, updmedia, medaction)
            show_geo_bo, show_web_bo = determine_dropdown_behavior(updmedia)

        elif request.args.get('action') == "GenerateMediaforCreate":
            provider = request.form.get("provider")
            network = request.form.get("network")
            mediaid = request.form.get("program")
            medaction = request.form.get("medAction")
            media = request.form.get("updMediaxml")
            generate_media_for_create(mediaid, medaction, network)
            updmedia = media

        elif request.args.get('action') == "GenerateMediaforRemove":
            provider = request.form.get("provider")
            network = request.form.get("network")
            mediaid = request.form.get("program")
            medaction = request.form.get("medAction")
            media = request.form.get("updMediaxml")
            generate_media_for_remove(mediaid, network)
            updmedia = media

        elif request.args.get('action') == "RemoveMediaPoint":
            provider = request.form.get("provider")
            network = request.form.get("network")
            mediaid = request.form.get("program")
            media = request.form.get("updMediaxml")
            medaction = request.form.get("medAction")
            remove_mediapoint(mediaid)
            updmedia = media

        elif request.args.get('action') == "posttocdadent":
            provider = request.form.get("provider")
            network = request.form.get("network")
            mediaid = request.form.get("program")
            medaction = request.form.get("medAction")
            updmedia = request.form.get("updMediaxml")


            if provider == "FOX":
                action = 'update'
            else:
                action = request.form.get("action")

            if action == 'CopyUpdate':
                updmedia = copy_media(updmedia, mediaid)

            actual_mediaid = parse_mediaid(updmedia)


            cad_res = post_media_to_cadent(provider, network, actual_mediaid, updmedia, action)
#            provider = ''
#            mediaid = ''
#            network = ''
#            media = ''
#            programs = []
        else:
            media = ''
            programs = []
    except Exception as mainerr:
        logger.error(mainerr.message)
    return render_template('Blackout_Scheduler.html', progid=mediaid, updatedMedia=updmedia, network=network,
                           programs=programs, provider=provider, medAction=medaction, cadent_response=cad_res,
                           show_geo_bo=show_geo_bo, show_web_bo=show_web_bo)


# Create Disney Blackout Start
def create_disney_bo_in_cadent(network, mediaid, body):
    """
    Send put request to cadent end point to create the blackout
    :param network: ESPN, ESPN2, ESPNU, DEPORTES
    :param mediaid: uuid of the program to be blacked out
    :param body: 224 that will be the data of the put request
    :return: String, the Cadent response of form {response code}-{response text}
    """
    cadent_url = r"https://api-chtr41.cadent-labs.tv/altcontentsvc/esni2018/Charter/Disney/disney.com/{}/program/{}"\
        .format(network, mediaid)
    headers = {'Content-Type': 'application/xml',
               'Accept': "*/*",
               'Connection': 'keep-alive',
               'Accept-Encoding': 'gzip,deflacet,br'
               }
    program_listing_response = requests.put(cadent_url, headers=headers, data=body.encode('utf-8'))
    return "{}-{}".format(program_listing_response.status_code, program_listing_response.text)


def get_disney_programs(channel, blackouttype):
    """
    queries the ESPN PCC to get program information. If blackouttype is a match time blackout, this method will return
    the current program. If the blackouttype is not a match time blackout it will return all future listings until
    midnight MST, excluding the currently playing program
    :param channel: ESPN, ESPN2, ESPNU, DEPORTES
    :param blackouttype: Geo Blackout, Geo Blackout with Matchtime, Device Blackout, Device Blackout with Matchtime
    :return: List(String) list of programs based on blackouttype
    """

    disney_pcc_url = r"http://watch.video.api.espn.com/video/api/airings"

    if "Matchtime" in blackouttype:
        params = {"network": channel,
                  "at": "NOW",
                  "apikey": "133qcu6jduxwc1t8hk2r1uy1qq",
                  "includeProperties": ''}
    else:
        # get current program end time
        _, first_time, _ = parse_program(
            parse_disney_listing_resp(get_disney_programs(channel, "Matchtime"), show_uuid=False)[0],
            uuid_present=False)

        # add a minute to help with query borders
        first_time = dt.strptime(first_time[:-4], "%Y-%m-%dT%H:%M:00") + timedelta(minutes=1)

        # calculate end time (7am utc which is midnight mst)
        to_datetime = dt.utcnow()
        midnight_mst_diff = (24 - to_datetime.hour) + 6
        to_datetime += timedelta(hours=midnight_mst_diff, minutes=60-to_datetime.minute)

        from_datetime = first_time.strftime("%Y-%m-%dT%H:%M:00Z")
        to_datetime = to_datetime.strftime("%Y-%m-%dT%H:%M:00Z")

        params = {"network": channel,
                  "from": from_datetime,
                  "to": to_datetime,
                  "apikey": "133qcu6jduxwc1t8hk2r1uy1qq",
                  "includeProperties": ''}

    program_listing_response = requests.get(disney_pcc_url, params)

    return program_listing_response


def parse_disney_listing_resp(response, show_uuid=False):
    """
    Takes the http response from the espn pcc and parses the json, returning a list of strings representing the program
    schedule for whatever was requested from the "get_disney_programs" method.
    Each string in the return list is of the following form:
        {name}@{start time} - {end time} ~ {simulcast id} ~ {uuid}
    :param response: requests.Response object
    :param no_uuid: bool to determine if you want to include the uuid in the listing or not
    :return: List(string)
    """
    resp_content = json.loads(response.content)

    disney_listing = list()
    listing = None

    for row in resp_content["rows"]:
        # remove extra bit of timezone info we don't need
        start = row["start"].split('+')[0]
        end = row["end"].split('+')[0]

        if show_uuid:
            listing = "{}@{} to {} ~ {} ~ {}".format(
                row["properties"]["title"],
                start,
                end,
                row["properties"]["simulcastAiringId"],
                row["id"])
        else:
            listing = "{}@{} to {} ~ {}".format(
                row["properties"]["title"],
                start,
                end,
                row["properties"]["simulcastAiringId"])

        disney_listing.append(listing)

    disney_listing.sort(key=lambda x: x.split('@')[1])
    return disney_listing


def parse_program(program, uuid_present=True):
    """
    Each program in the progam dropdown is of the form:
        {name}@{start time} - {end time} ~ {simulcast id} ~ {uuid}
    This method takes in the raw string from the dropdown and parses it into each component,
    name, start time, end time, simulcast id, uuid
    :param program: string of the form {name}@{start time} - {end time} ~ {simulcast id} ~ {uuid}
    :param uuid_present: bool True == uuid is present in program string, False == uuid not present in program string
    :return: a tuple consisting of the parts of the channel string, name, start time, end time, simulcast id, uuid
    """

    # remove program name, not needed. Also regex? who needs it
    program = program.split('@')[1]
    program = program.split(' to ')

    strt_time = program[0]

    program = program[1]

    program = program.split(' ~ ')

    end_time = program[0]

    simulcastid = program[1]

    if uuid_present:
        uuid = program[2]

        return strt_time, end_time, simulcastid, uuid
    else:
        return strt_time, end_time, simulcastid



def render_disney_bo_template(bo_type, program, channel):
    """
    takes the parameters from the create disney blackout form, calculates matchtime, mediaeffective, startmpexpiry,
    endmpeffective, and mediaexpiry and returns the populated template corresponding to the bo_type
    :param bo_type: type of blackout the user has requested
    :param program: the program to be blacked out
    :param channel: ESPN, ESPN2, ESPNU, DEPORTES
    :return: string representation of 224 template corresponding to specific bo_type provided
    """
    env = Environment(
        loader=PackageLoader("Blackout_Scheduler"),
        autoescape=select_autoescape()
    )

    # set up variables we need to fill out blackout xml template
    effective_buffer = timedelta(minutes=Cfg.disney_effective_buffer)
    uuid = fetch_disney_uuid(channel, bo_type, program)
    strt_time, end_time, simulcastid = parse_program(program, uuid_present=False)

    strt_time = strt_time[:-4]
    end_time = end_time[:-4]

    strt_dt = dt.strptime(strt_time, "%Y-%m-%dT%H:%M:%S")
    end_dt = dt.strptime(end_time, "%Y-%m-%dT%H:%M:%S")

    # -6 hours
    mediaeff = (strt_dt - effective_buffer).strftime("%Y-%m-%dT%H:%M:00Z")
    startmpexpiry = (strt_dt + effective_buffer).strftime("%Y-%m-%dT%H:%M:00Z")

    endmpeff = (end_dt - effective_buffer).strftime("%Y-%m-%dT%H:%M:00Z")
    mediaexp = (end_dt + effective_buffer).strftime("%Y-%m-%dT%H:%M:00Z")

    timestamputc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4] + 'Z'
    matchtime = "calculated upon submit"


    if bo_type == "Geo Blackout":
        template = env.get_template("disney_geo_blackout.xml")
    elif bo_type == "Geo Blackout with Matchtime":
        template = env.get_template("disney_geo_matchtime_blackout.xml")
    elif bo_type == "Device Blackout":
        template = env.get_template("disney_device_blackout.xml")
    else:
        template = env.get_template("disney_device_matchtime_blackout.xml")

    return template.render(AiringID=simulcastid,
                           startmpexpiry=startmpexpiry,
                           MediaEffective=mediaeff,
                           MediaExpiry=mediaexp,
                           network=channel,
                           MediaID=uuid,
                           timestampUtcIso8601=timestamputc,
                           endmpeffective=endmpeff,
                           matchtime=matchtime)


def updateDisneyBoData(bo_xml, buffer):
    """
    Takes the Disney 224 xml that will be used to create a blackout and update the matchtime and lastupdated parameters
    for match time blackouts or just the lastupdated field for regular blackouts to reflect the time the user submitted
    the blackout

    :param bo_xml: the 224 xml taken from the "create disney blackout" form
    :param matchpoint_buffer: taken from the match point buffer field in the create disney bo form. In minutes
    :return: str containing 224 xml with updated matchtime and lastupdated parameters
    """


    matchtime_buffer = timedelta(minutes=int(buffer))
    matchtime = (dt.utcnow() + matchtime_buffer).strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4] + 'Z'

    timestamputc = dt.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4] + 'Z'

    try:
        tree = etree.ElementTree(etree.fromstring(bo_xml))
        nsmap = {'ns': 'http://www.scte.org/schemas/224'}
        root = tree.getroot()
        root.set('lastUpdated', timestamputc)

        mediapoints = root.findall("ns:MediaPoint", nsmap)
        for mediapoint in mediapoints:
            if "matchTime" in [t[0] for t in mediapoint.attrib.items()]:
                mediapoint.set('matchTime', matchtime)

            mediapoint.set('lastUpdated', timestamputc)

        return etree.tostring(root)

    except Exception as e:
        raise e

    return "error in updating disney bo when submitting"


def fetch_disney_uuid(channel, bo_type, selected_program):
    """
    Since i'm not including uuid in program listing in the create disney form, this method is used to get that uuid for
    a selected program
    :param bo_type: type of blackout the user has requested
    :param selected_program: the program whose uuid we want to fetch
    :param channel: ESPN, ESPN2, ESPNU, DEPORTES
    :return: str uuid
    """
    programslisting = parse_disney_listing_resp(get_disney_programs(channel, bo_type), show_uuid=True)
    for program in programslisting:
        if selected_program in program:
            _, _, _, uuid = parse_program(program, uuid_present=True)
            return uuid


@app.route("/DisneyCreate", methods=('get', 'post'))
def createbo():
    channel = ''
    program = ''
    blackouttype = ''
    updatedmedia = ''
    programslisting = []
    buff = "1"
    cadentresponse = ''
    show_buffer = False

    try:
        if request.args.get('action') == 'getprograms':
            channel = request.form.get("channel")
            blackouttype = request.form.get("blackouttype")
            programslisting = parse_disney_listing_resp(get_disney_programs(channel, blackouttype), show_uuid=False)
            show_buffer = "Matchtime" in blackouttype

        elif request.args.get('action') == 'makeblackout':
            channel = request.form.get("channel")
            blackouttype = request.form.get("blackouttype")
            programslisting = parse_disney_listing_resp(get_disney_programs(channel, blackouttype), show_uuid=False)
            program = request.form.get("programs")
            show_buffer = "Matchtime" in blackouttype
            if show_buffer:
                buff = request.form.get("buffer")

            updatedmedia = render_disney_bo_template(blackouttype, program, channel)

        elif request.args.get('action') == 'submitblackout':
            channel = request.form.get("channel")
            blackouttype = request.form.get("blackouttype")
            programslisting = get_disney_programs(channel, blackouttype)
            program = request.form.get("programs")
            buff = request.form.get("buffer")

            updatedmedia = updateDisneyBoData(request.form.get("updMediaxml"), buff)

            uuid = fetch_disney_uuid(channel, blackouttype, program)

            cadentresponse = str(create_disney_bo_in_cadent(channel, uuid, updatedmedia))

        return render_template('Disney_Blackout_Generator.html', channel_input=channel, program=program,
                               programs=programslisting, blackouttype=blackouttype, updatedMedia=updatedmedia,
                               buffer=buff, cadentResponse=cadentresponse, show_buffer=show_buffer)

    except Exception as mainerr:
        logger.error(mainerr.message)
    return render_template('Disney_Blackout_Generator.html', channel_input=channel, program=program,
                           programs=programslisting, blackouttype=blackouttype, updatedMedia=updatedmedia,
                           buffer=buff, cadentResponse=cadentresponse, show_buffer=show_buffer)


if __name__ == '__main__':
    print('running app...')
    app.run(host='0.0.0.0', port='7002')
    print('----app is running-----')
