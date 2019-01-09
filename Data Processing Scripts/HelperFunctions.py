import xml.etree.ElementTree as Et
import csv

# Papers owned by Reviewers
paper_reviewer = {}
# Papers owned by ACs
paper_metareviewer = {}
# reviewer to paper
reviewer_paper = {}


# This function parses the paper to reviewer and AC extracted from CMT
def parse_files():
    # Assignment Paper to Reviewer
    # Links XML extracted from CML
    r_tree = Et.parse('./Files/Assignments_7pm_12Jul.xml')

    # meta reviewer assignment
    mr_tree = Et.parse('./Files/MetaAssignments_7pm12Jul.xml')

    r_root = r_tree.getroot()
    mr_root = mr_tree.getroot()

    # get paper to reviewer mapping
    for subs in r_root.iter('submission'):
        subid = subs.attrib['submissionId']

        for reviewers in subs.iter('user'):
            if subid not in paper_reviewer.keys():
                paper_reviewer[subid] = []

            if reviewers.attrib['email'] not in reviewer_paper.keys():
                reviewer_paper[reviewers.attrib['email']] = []

            paper_reviewer[subid].append(reviewers.attrib['email'])
            reviewer_paper[reviewers.attrib['email']].append(subid)

    # get paper to Meta reviewer mapping
    for subs in mr_root.iter('submission'):
        subid = subs.attrib['submissionId']

        for meta_reviewers in subs.iter('user'):
            paper_metareviewer[subid] = meta_reviewers.attrib['email']


# mapping between meta reviewers and their reviewers
# Dependency Parse_files
ac_to_reviewer_mapping = {}


# meta-reviewers to reviewers mapping created
# needs parse file as dependency
def create_ac_to_reviewers():
    # crete mapping
    for paper_id, meta in paper_metareviewer.items():

        if meta not in ac_to_reviewer_mapping.keys():
            ac_to_reviewer_mapping[meta] = []

        for reviewer in paper_reviewer[paper_id]:
            if reviewer not in ac_to_reviewer_mapping[meta]:
                ac_to_reviewer_mapping[meta].append(reviewer)


# Reviewer as index
# Dependency Parse_files
reviewer_to_ac_mapping = {}


# Reviewers to Meta-Reviewers mapping
def create_reviewer_to_ac():
    # crete mapping
    for paper_id, meta in paper_reviewer.items():

        try:
            for i in meta:
                if i not in reviewer_to_ac_mapping.keys():
                    reviewer_to_ac_mapping[i] = []

                if paper_metareviewer[paper_id] not in reviewer_to_ac_mapping[i]:
                    reviewer_to_ac_mapping[i].append(paper_metareviewer[paper_id])
        except:
            print("No AC for:")
            print(paper_id)


# All incomplete papers
# Dependency: None
incomplete_ids = []


# Read Ids of file from the submission table
def incomplete_submissions_table_read():
    with open('./Files/incomplete_papers_7pm12Jul.csv', encoding='utf-8') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            incomplete_ids.append(row[0].split(' ')[0])


# ACs mapped to incomplete papers
# Dependency Incomplete Papers, Parse Files; Out incomplete_paper_AC
incomplete_paper_AC = {}


# AC to incomplete paper mapping
def incomplete_papers_ac_mapping():
    for paperid in incomplete_ids:

        try:
            if paper_metareviewer[paperid] not in incomplete_paper_AC.keys():
                incomplete_paper_AC[paper_metareviewer[paperid]] = []

            incomplete_paper_AC[paper_metareviewer[paperid]].append(paperid)
        except:
            print(paperid)


# SAC, AC email to name mapping
# Dependency: None
ac_email_to_name = {}


def get_ac_sac_email_names():
    ac_sac_email_names = {}
    # Mapping between Names and email of AC and SACS
    with open('./Files/Email-NamesSAC&AC.tsv', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for name, lastname, email, _, _ in reader:
            ac_email_to_name[email] = "{} {}".format(name, lastname)
    # return ac_sac_email_names


# Sac to AC mapping
# Dependency None
sac_to_ac = {}

ac_to_sac = {}

def sac_to_ac_mapping():
    c = 0
    # Mapping between Senior MetaReviewer and MetaReviewer
    with open('./Files/SMR__MR_mappings.txt') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if c == 0:
                c += 1
                continue

            if row[0] not in sac_to_ac:
                sac_to_ac[row[0]] = []

            sac_to_ac[row[0]].append(row[1])

            ac_to_sac[row[1]] = row[0]

# Get emails of not logged in
# Dependency: None
reviewers_not_logged = []


def email_of_not_logged_in():
    c = 0
    with open('./Files/Reviewers_notlogged_19thJune.csv', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if c < 2:
                c += 1
                continue

            reviewers_not_logged.append(row[2])


# Get papers assigned to list of reviewers
# Dependency parse_files
paper_assigned_to_reviewers = {}
paper_assigned_to_reviewers_inverted = {}


def papers_assigned_to_list_of_reviewers(list_of_reviewers):
    for reviewer in list_of_reviewers:
        if reviewer in reviewer_paper:
            paper_assigned_to_reviewers[reviewer] = reviewer_paper[reviewer]

    for reviewer in list_of_reviewers:
        if reviewer in reviewer_paper:
            for paper in reviewer_paper[reviewer]:
                if paper not in paper_assigned_to_reviewers_inverted:
                    paper_assigned_to_reviewers_inverted[paper] = []

                paper_assigned_to_reviewers_inverted[paper].append(reviewer)


# sac_to_ac_mapping()
# print(sac_to_ac)

# parse_files()
# email_of_not_logged_in()
# papers_assigned_to_list_of_reviewers(reviewers_not_logged)
#
# print(paper_assigned_to_reviewers)

# email_of_not_logged_in()
#
# print(reviewers_not_logged)

# create_reviewer_to_ac()

# incomplete_submissions_table_read()
# incomplete_papers_ac_mapping()
# get_ac_sac_email_names()
#
# send_chase_email_to_ac()
