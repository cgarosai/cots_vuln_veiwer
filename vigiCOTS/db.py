import psycopg2
from dotenv import load_dotenv
import os
import logging

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        return conn
    except Exception as e:
        error_msg = str(e)
        raise ConnectionError("Erreur lors de la connexion à la base de données:  "+ error_msg)
    

def fetch_cves_by_cpe(cpe, cvss_min):
    query = '''
            WITH searched_cves AS (
                SELECT DISTINCT cc.cves_id
                FROM cots_cves cc
                WHERE cc.cots_id IN (
                    SELECT id FROM cots 
                    WHERE cpe = %s
                )
            )
            SELECT 
                cve.name,
                cve.cwe,
                cve.summary,
                cvss.cvss,
                cve.published::date,
                cve.last_modified,
                cve.exploit,
                cvss3_vector.attack_complexity, cvss3_vector.attack_vector, cvss3_vector.privileges_required, cvss3_vector.user_interaction
            FROM searched_cves lkc
            JOIN cve ON cve.id = lkc.cves_id
            LEFT JOIN cvss3_mark cvss ON cvss.cve_id = cve.id
            JOIN cvss3_vector ON cvss.vector_id = cvss3_vector.id
            WHERE COALESCE(cvss.cvss, 0) >= %s;
    '''
    if cvss_min != 0:
        inputs = (cpe, cvss_min)
    else: 
        inputs = (cpe,0)
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, inputs)
            return cur.fetchall()



def fetch_cves_by_name(name, cvss_min):
    query = '''
            WITH searched_cves AS (
                SELECT DISTINCT cc.cves_id
                FROM cots_cves cc
                WHERE cc.cots_id IN (
                    SELECT id FROM cots 
                    WHERE name = %s
                )
            )
            SELECT 
                cve.name,
                cve.cwe,
                cve.summary,
                cvss.cvss,
                cve.published::date,
                cve.last_modified,
                cve.exploit,
                cvss3_vector.attack_complexity, cvss3_vector.attack_vector, cvss3_vector.privileges_required, cvss3_vector.user_interaction
            FROM searched_cves lkc
            JOIN cve ON cve.id = lkc.cves_id
            LEFT JOIN cvss3_mark cvss ON cvss.cve_id = cve.id
            JOIN cvss3_vector ON cvss.vector_id = cvss3_vector.id
            WHERE COALESCE(cvss.cvss, 0) >= %s;
    '''
    if cvss_min != 0:
        inputs = (name, cvss_min)
    else: 
        inputs = (name,0)
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, inputs)
            return cur.fetchall()

def fetch_cves_by_name_version(name, version, cvss_min):
    query = '''
        WITH version_cots AS (
            SELECT id FROM cots 
            WHERE name = %s AND version = %s
        ),
        version_cves AS (
            SELECT DISTINCT cc.cves_id
            FROM cots_cves cc
            WHERE cc.cots_id IN (SELECT id FROM version_cots)
        )
        SELECT 
            cve.name,
            cve.cwe,
            cve.summary,
            cvss.cvss,
            cve.published::date,
            cve.last_modified,
            cve.exploit,
            cvss3_vector.attack_complexity, cvss3_vector.attack_vector, cvss3_vector.privileges_required, cvss3_vector.user_interaction
        FROM version_cves vc
        JOIN cve ON cve.id = vc.cves_id
        LEFT JOIN cvss3_mark cvss ON cvss.cve_id = cve.id
        JOIN cvss3_vector ON cvss.vector_id = cvss3_vector.id
        WHERE COALESCE(cvss.cvss, 0) >= %s
    '''
    if cvss_min != 0:
        inputs = (name, version, cvss_min)
    else: 
        inputs = (name, version, 0) 
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, inputs)
            return cur.fetchall()


def fetch_cots_by_guessed_name(name):
    query = '''
        SELECT name, version, cpe 
        FROM cots
        WHERE name ILIKE %s ESCAPE '';
    '''
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, ('%' + name + '%',))
            return cur.fetchall()
        


def fetch_cots_by_guessed_provider(name, provider):
    query = '''
        SELECT name, version, cpe 
        FROM cots
        WHERE cpe ILIKE %s ESCAPE '';
    '''
    search = '%' + provider + '%'
    if name.strip() != '':
        search += ':%' + name + '%'
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (search,))
            return cur.fetchall()
    