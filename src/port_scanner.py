import socket
import threading
import time
from urllib.parse import urlparse

from src.display import GREEN, RED, RESET

COMMON_PORTS = [
    20,21,22,23,25,26,53,67,68,69,79,80,81,82,83,84,85,88,110,111,
    119,123,135,137,138,139,143,161,162,179,194,220,389,443,444,445,
    465,500,502,512,513,514,515,520,587,623,631,636,873,902,993,995,
    1080,1194,1433,1434,1521,1604,1723,1883,1900,2049,2082,2083,2086,
    2087,2095,2096,2121,2181,2375,2376,2379,2380,3000,3001,3128,3260,
    3299,3306,3389,3690,4000,4001,4040,4200,4369,4444,4500,4567,4848,
    5000,5001,5004,5005,5060,5061,5353,5432,5601,5672,5900,5984,6000,
    6379,6443,6667,6881,7070,7077,7443,7474,7687,8000,8001,8008,8009,
    8010,8069,8080,8081,8082,8083,8086,8087,8088,8089,8161,8443,8444,
    8545,8888,8983,9000,9001,9042,9090,9092,9093,9200,9300,9418,9999,
    10000,10001,10250,10255,11211,15672,15692,16379,16686,27017,27018,
    27019,28015,28017,50000,50070,50075,54321,55672,61616,
]

SERVICES = {
    20:"FTP-data",21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",26:"SMTP-alt",
    53:"DNS",67:"DHCP",68:"DHCP",69:"TFTP",79:"Finger",80:"HTTP",
    81:"HTTP-alt",82:"HTTP-alt",83:"HTTP-alt",84:"HTTP-alt",85:"HTTP-alt",
    88:"Kerberos",110:"POP3",111:"RPCbind",119:"NNTP",123:"NTP",
    135:"RPC",137:"NetBIOS",138:"NetBIOS",139:"NetBIOS",143:"IMAP",
    161:"SNMP",162:"SNMP-trap",179:"BGP",194:"IRC",220:"IMAP3",
    389:"LDAP",443:"HTTPS",444:"SNPP",445:"SMB",465:"SMTPS",
    500:"IKE",502:"Modbus",512:"rexec",513:"rlogin",514:"Syslog",
    515:"LPD",520:"RIP",587:"SMTP",623:"IPMI",631:"IPP",636:"LDAPS",
    873:"rsync",902:"VMware",993:"IMAPS",995:"POP3S",1080:"SOCKS",
    1194:"OpenVPN",1433:"MSSQL",1434:"MSSQL-UDP",1521:"Oracle",
    1604:"Citrix",1723:"PPTP",1883:"MQTT",1900:"UPnP",2049:"NFS",
    2082:"cPanel",2083:"cPanel-SSL",2086:"WHM",2087:"WHM-SSL",
    2095:"cPanel-Mail",2096:"cPanel-Mail-SSL",2121:"FTP-alt",
    2181:"Zookeeper",2375:"Docker",2376:"Docker-SSL",2379:"etcd",
    2380:"etcd-peer",3000:"Grafana",3001:"Node-dev",3128:"Squid",
    3260:"iSCSI",3299:"SAP",3306:"MySQL",3389:"RDP",3690:"SVN",
    4000:"alt-HTTP",4001:"alt-HTTP",4040:"Spark-UI",4200:"Angular-dev",
    4369:"EPMD",4444:"Metasploit",4500:"IKE-NAT",4567:"Sinatra",
    4848:"GlassFish",5000:"Flask-dev",5001:"alt-HTTPS",5004:"RTP",
    5005:"RTP",5060:"SIP",5061:"SIP-TLS",5353:"mDNS",5432:"PostgreSQL",
    5601:"Kibana",5672:"AMQP",5900:"VNC",5984:"CouchDB",6000:"X11",
    6379:"Redis",6443:"Kubernetes",6667:"IRC",6881:"BitTorrent",
    7070:"RealAudio",7077:"Spark",7443:"HTTPS-alt",7474:"Neo4j",
    7687:"Bolt",8000:"HTTP-alt",8001:"HTTP-alt",8008:"HTTP-alt",
    8009:"AJP",8010:"HTTP-alt",8069:"Odoo",8080:"HTTP-proxy",
    8081:"HTTP-alt",8082:"HTTP-alt",8083:"HTTP-alt",8086:"InfluxDB",
    8087:"Riak",8088:"HTTP-alt",8089:"Splunk",8161:"ActiveMQ",
    8443:"HTTPS-alt",8444:"HTTPS-alt",8545:"Ethereum-RPC",
    8888:"HTTP-alt",8983:"Solr",9000:"PHP-FPM",9001:"Supervisor",
    9042:"Cassandra",9090:"Prometheus",9092:"Kafka",9093:"Kafka-SSL",
    9200:"Elasticsearch",9300:"Elasticsearch-cluster",9418:"Git",
    9999:"alt-HTTP",10000:"Webmin",10001:"alt-TCP",10250:"Kubelet",
    10255:"Kubelet-ro",11211:"Memcached",15672:"RabbitMQ-UI",
    15692:"RabbitMQ-metrics",16379:"Redis-cluster",16686:"Jaeger",
    27017:"MongoDB",27018:"MongoDB",27019:"MongoDB",28015:"RethinkDB",
    28017:"MongoDB-HTTP",50000:"SAP",50070:"HDFS-NameNode",
    50075:"HDFS-DataNode",54321:"H2O",55672:"RabbitMQ",61616:"ActiveMQ",
}

TIMEOUT = 0.5


def _host(url):
    parsed = urlparse(url)
    return parsed.hostname or parsed.path or url


def _scan_port(host, port, open_ports, lock):
    try:
        with socket.create_connection((host, port), timeout=TIMEOUT):
            with lock:
                open_ports.append(port)
    except Exception:
        pass


def run_portscan(url, any_flag, select_ports):
    host  = _host(url)
    ports = COMMON_PORTS if any_flag else select_ports
    label = f"common ({len(ports)})" if any_flag else ", ".join(str(p) for p in ports)

    print(f"  Port scan  {host}")
    print(f"  Ports: {label}")
    print()

    open_ports = []
    lock       = threading.Lock()
    threads    = [
        threading.Thread(target=_scan_port, args=(host, p, open_ports, lock))
        for p in ports
    ]

    start = time.perf_counter()
    for t in threads: t.start()
    for t in threads: t.join()
    elapsed = time.perf_counter() - start

    open_ports.sort()

    if open_ports:
        print(f"  {'PORT':<8} SERVICE")
        for p in open_ports:
            svc = SERVICES.get(p, "unknown")
            print(f"  {p:<8} {svc}  {GREEN}open{RESET}")
    else:
        print("  No open ports found.")

    print()
    print(f"  Scanned {len(ports)} ports in {elapsed:.2f}s  {len(open_ports)} open")
