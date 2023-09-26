#!/usr/bin/env python3

"""
name2username by Kali Nathalie (github.com/kalinathalie)
"""

import argparse
import re
import os

class PC:
    """PC (Print Color)
    Used to generate some colorful, relevant, nicely formatted status messages.
    """
    green = '\033[92m'
    blue = '\033[94m'
    orange = '\033[93m'
    endc = '\033[0m'
    ok_box = blue + '[*] ' + endc
    note_box = green + '[+] ' + endc
    warn_box = orange + '[!] ' + endc

def parse_arguments():
    """
    Handle user-supplied arguments
    """
    desc = ('name2username by Kali Nathalie (github.com/kalinathalie)')
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-f', '--filename', type=str, action='store', required=True,
                        help='Specify your Filename to read each name and.'
                        'transform into usernames.'
                        )
    parser.add_argument('-d', '--domain', type=str, action='store', required=True,
                        default='',
                        help='Append a domain name to username output. '
                        '[example: "-n uber.com" would output jschmoe@uber.com]'
                        )
    parser.add_argument('-c', '--complete', type=str, action='store', required=True,
                        default='',
                        help='Verify if you wanna all the outputs in one single file'
                        'need to be True or False'
                        )

    args = parser.parse_args()

    if not args.complete in ["True", "False"]:
        print("Error in --complete.")
        exit(1)
    if args.complete == "True":
        args.complete = True
    else:
        args.complete = False

    # If appending an email address, preparing this string now:
    if args.domain:
        args.domain = '@' + args.domain

    return args

def remove_accents(raw_text):
    """Removes common accent characters.
    Our goal is to brute force login mechanisms, and I work primary with
    companies deploying English-language systems. From my experience, user
    accounts tend to be created without special accented characters. This
    function tries to swap those out for standard English alphabet.
    """

    raw_text = re.sub(u"[àáâãäå]", 'a', raw_text)
    raw_text = re.sub(u"[èéêë]", 'e', raw_text)
    raw_text = re.sub(u"[ìíîï]", 'i', raw_text)
    raw_text = re.sub(u"[òóôõö]", 'o', raw_text)
    raw_text = re.sub(u"[ùúûü]", 'u', raw_text)
    raw_text = re.sub(u"[ýÿ]", 'y', raw_text)
    raw_text = re.sub(u"[ß]", 'ss', raw_text)
    raw_text = re.sub(u"[ñ]", 'n', raw_text)
    return raw_text

def clean(raw_list):
    """Removes common punctuation.
    This function is based on what I have seen in large searches, and attempts
    to remove them.
    """
    clean_list = []
    allowed_chars = re.compile('[^a-zA-Z -]')
    for name in raw_list:

        # Lower-case everything to make it easier to de-duplicate.
        name = name.lower()
      
        # Try to transform non-English characters below.
        name = remove_accents(name)

        # The line below basically trashes anything weird left over.
        # A lot of users have funny things in their names, like () or ''
        # People like to feel special, I guess.
        name = allowed_chars.sub('', name)

        # The line below tries to consolidate white space between words
        # and get rid of leading/trailing spaces.
        name = re.sub(r'\s+', ' ', name).strip()

        # If what is left is non-empty and unique, we add it to the list.
        if name and name not in clean_list:
            clean_list.append(name)

    return clean_list

def read_file(filename):
    with open(filename) as file:
        return file.readlines()

def write_files(domain, name_list, complete):
    out_dir = 'n2un-output'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    company = domain[1:]
    # Define all the files names we will be creating.
    files = {}
    if not complete:
        files['f.last'] = open(out_dir + '/' + company + '-f.last.txt', 'w')
        files['flast'] = open(out_dir + '/' + company + '-flast.txt', 'w')
        files['firstl'] = open(out_dir + '/' + company + '-firstl.txt', 'w')
        files['firstlast'] = open(out_dir + '/' + company + '-first.last.txt', 'w')
        files['fonly'] = open(out_dir + '/' + company + '-first.txt', 'w')
        files['lastf'] = open(out_dir + '/' + company + '-lastf.txt', 'w')
    else:
        files['complete'] = open(out_dir + '/' + company + '-complete.txt', 'w')

    # First, write all the raw names to a file.
    for name in name_list:
        
        # Split the name on spaces and hyphens:
        parse = re.split(' |-', name)
        
        try:
            if not complete:
                if len(parse) >= 4:
                    first, second, third, fourth = parse[0], parse[-3], parse[-2], parse[-1]
                    files['flast'].write(first[0] + second + domain + '\n')
                    files['flast'].write(first[0] + third + domain + '\n')
                    files['flast'].write(first[0] + fourth + domain + '\n')
                    files['f.last'].write(first[0] + '.' + second + domain + '\n')
                    files['f.last'].write(first[0] + '.' + third + domain + '\n')
                    files['f.last'].write(first[0] + '.' + fourth + domain + '\n')
                    files['lastf'].write(second + first[0] + domain + '\n')
                    files['lastf'].write(third + first[0] + domain + '\n')
                    files['lastf'].write(fourth + first[0] + domain + '\n')
                    files['firstlast'].write(first + '.' + second + domain + '\n')
                    files['firstlast'].write(first + '.' + third + domain + '\n')
                    files['firstlast'].write(first + '.' + fourth + domain + '\n')
                    files['firstl'].write(first + second[0] + domain + '\n')
                    files['firstl'].write(first + third[0] + domain + '\n')
                    files['firstl'].write(first + fourth[0] + domain + '\n')
                    files['fonly'].write(first + domain + '\n')
                    files['sonly'].write(second + domain + '\n')
                    files['tonly'].write(third + domain + '\n')
                    files['fonly'].write(fourth + domain + '\n')
                    files['lastfirst'].write(fourth + '.' + first + domain + '\n')
                    files['lastfirst'].write(third + '.' + first + domain + '\n')
                    files['lastfirst'].write(second + '.' + first + domain + '\n')
                if len(parse) == 3:  # for users with more than one last name.
                    first, second, third = parse[0], parse[-2], parse[-1]
                    files['flast'].write(first[0] + second + domain + '\n')
                    files['flast'].write(first[0] + third + domain + '\n')
                    files['f.last'].write(first[0] + '.' + second + domain + '\n')
                    files['f.last'].write(first[0] + '.' + third + domain + '\n')
                    files['lastf'].write(second + first[0] + domain + '\n')
                    files['lastf'].write(third + first[0] + domain + '\n')
                    files['firstlast'].write(first + '.' + second + domain + '\n')
                    files['firstlast'].write(first + '.' + third + domain + '\n')
                    files['firstl'].write(first + second[0] + domain + '\n')
                    files['firstl'].write(first + third[0] + domain + '\n')
                    files['fonly'].write(first + domain + '\n')
                    files['sonly'].write(second + domain + '\n')
                    files['tonly'].write(third + domain + '\n')
                    files['lastfirst'].write(third + '.' + first + domain + '\n')
                    files['lastfirst'].write(second + '.' + first + domain + '\n')
                else:               # for users with only one last name
                    first, last = parse[0], parse[-1]
                    files['flast'].write(first[0] + last + domain + '\n')
                    files['f.last'].write(first[0] + '.' + last + domain + '\n')
                    files['lastf'].write(last + first[0] + domain + '\n')
                    files['firstlast'].write(first + '.' + last + domain + '\n')
                    files['firstl'].write(first + last[0] + domain + '\n')
                    files['fonly'].write(first + domain + '\n')
                    files['sonly'].write(last + domain + '\n')
                    files['lastfirst'].write(last + '.' + first + domain + '\n')
            else:
                if len(parse) >= 4:
                    first, second, third, fourth = parse[0], parse[-3], parse[-2], parse[-1]
                    files['complete'].write(first[0] + second + domain + '\n')
                    files['complete'].write(first[0] + third + domain + '\n')
                    files['complete'].write(first[0] + fourth + domain + '\n')
                    files['complete'].write(first[0] + '.' + second + domain + '\n')
                    files['complete'].write(first[0] + '.' + third + domain + '\n')
                    files['complete'].write(first[0] + '.' + fourth + domain + '\n')
                    files['complete'].write(second + first[0] + domain + '\n')
                    files['complete'].write(third + first[0] + domain + '\n')
                    files['complete'].write(fourth + first[0] + domain + '\n')
                    files['complete'].write(first + '.' + second + domain + '\n')
                    files['complete'].write(first + '.' + third + domain + '\n')
                    files['complete'].write(first + '.' + fourth + domain + '\n')
                    files['complete'].write(first + second[0] + domain + '\n')
                    files['complete'].write(first + third[0] + domain + '\n')
                    files['complete'].write(first + fourth[0] + domain + '\n')
                    files['complete'].write(first + domain + '\n')
                    files['complete'].write(second + domain + '\n')
                    files['complete'].write(third + domain + '\n')
                    files['complete'].write(fourth + domain + '\n')
                    files['complete'].write(fourth + '.' + first + domain + '\n')
                    files['complete'].write(third + '.' + first + domain + '\n')
                    files['complete'].write(second + '.' + first + domain + '\n')
                if len(parse) == 3:  # for users with more than one last name.
                    first, second, third = parse[0], parse[-2], parse[-1]
                    files['complete'].write(first[0] + second + domain + '\n')
                    files['complete'].write(first[0] + third + domain + '\n')
                    files['complete'].write(first[0] + '.' + second + domain + '\n')
                    files['complete'].write(first[0] + '.' + third + domain + '\n')
                    files['complete'].write(second + first[0] + domain + '\n')
                    files['complete'].write(third + first[0] + domain + '\n')
                    files['complete'].write(first + '.' + second + domain + '\n')
                    files['complete'].write(first + '.' + third + domain + '\n')
                    files['complete'].write(first + second[0] + domain + '\n')
                    files['complete'].write(first + third[0] + domain + '\n')
                    files['complete'].write(first + domain + '\n')
                    files['complete'].write(second + domain + '\n')
                    files['complete'].write(third + domain + '\n')
                    files['complete'].write(third + '.' + first + domain + '\n')
                    files['complete'].write(second + '.' + first + domain + '\n')
                else:               # for users with only one last name
                    first, last = parse[0], parse[-1]
                    files['complete'].write(first[0] + last + domain + '\n')
                    files['complete'].write(first[0] + '.' + last + domain + '\n')
                    files['complete'].write(last + first[0] + domain + '\n')
                    files['complete'].write(first + '.' + last + domain + '\n')
                    files['complete'].write(first + last[0] + domain + '\n')
                    files['complete'].write(first + domain + '\n')
                    files['complete'].write(last + domain + '\n')
                    files['complete'].write(last + '.' + first + domain + '\n')


        # The exception below will try to weed out string processing errors
        # I've made in other parts of the program.
        except IndexError:
            print(PC.warn_box + "Struggled with this tricky name: '{}'."
                  .format(name))

    # Cleanly close all the files.
    for file_name in files:
        files[file_name].close()


def main():
    """Main Function"""
    args = parse_arguments()

    get_names = read_file(args.filename)

    clean_list = clean(get_names)

    write_files(args.domain, clean_list, args.complete)

    print("\n\n" + PC.ok_box + "All done! Check out your lovely new files in"
          "the n2un-output directory.")

if __name__ == "__main__":
    main()
