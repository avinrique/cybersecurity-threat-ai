import pandas as pd

# The 41 connection features, in the order they appear in the NSL-KDD files
FEATURES = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment',
    'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted',
    'num_root', 'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds',
    'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate',
    'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
    'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
    'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate',
]

# Features that hold text rather than numbers
TEXT_FEATURES = ['protocol_type', 'service', 'flag']

# Attack name -> the attack type the model predicts
ATTACK_TYPES = {
    **{a: "dos" for a in "back land neptune pod smurf teardrop apache2 udpstorm processtable mailbomb".split()},
    **{a: "probe" for a in "satan ipsweep nmap portsweep mscan saint".split()},
    **{a: "r2l" for a in "guess_passwd ftp_write imap phf multihop warezmaster warezclient spy xlock xsnoop "
                         "snmpguess snmpgetattack httptunnel sendmail named worm".split()},
    **{a: "u2r" for a in "buffer_overflow loadmodule rootkit perl sqlattack xterm ps".split()},
    "normal": "normal",
}


# Load an NSL-KDD .txt file and add the attack type of each connection
def load_connections(path):
    df = pd.read_csv(path, names=FEATURES + ["attack", "difficulty"])
    df["attack_type"] = df["attack"].map(ATTACK_TYPES)
    return df
