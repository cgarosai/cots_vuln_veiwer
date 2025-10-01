from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages, Response
from db import fetch_cves_by_cpe,fetch_cves_by_name, fetch_cves_by_name_version, fetch_cots_by_guessed_name, fetch_cots_by_guessed_provider

searchPage = Blueprint('searchPage', __name__)
resultPage = Blueprint('resultPage', __name__)


@searchPage.route('/', methods=['GET'])
def index():
    messages = get_flashed_messages(with_categories=True)
        # Re-créer les messages pour le template
    for category, message in messages:
        flash(message, category)
    return render_template('base.html', messages=messages)


@searchPage.route('/search_cots', methods=['POST'])
def search_cots():
    form = request.form
    guessed_name = form.get('guessed_name', '').strip()
    guessed_provider = form.get('guessed_provider', '').strip()
    # Validation
    if not guessed_name and not guessed_provider:
        return render_template('partials/error.html', message="Pour rechercher un COTS, renseignez un nom potentiel de COTS")

    redirect_url = url_for('resultPage.cots_results', 
                        guessed_name=guessed_name, 
                        guessed_provider=guessed_provider)
    response = Response("")
    response.headers['HX-Redirect'] = redirect_url
    return response

@searchPage.route('/search_cve', methods=['POST'])
def search_cve():

    form = request.form

    user_cpe = form.get('cpe') or form.get('cpe2')
    cots_name = form.get('name', '').strip()
    version = form.get('version', '').strip()
    cvss_min = form.get('min-CVSS', '0')

        # Validation
    if not user_cpe and not cots_name:
        return render_template("partials/error.html", message="Pour rechercher, utilisez SOIT le CPE du COTS, soit le couple NOM, VERSION, vous pouvez mettre any ou * pour avoir toutes les versions du COTS")

    # Redirection vers GET avec paramètres
    redirect_url = url_for('resultPage.cve_results',
                           cpe=user_cpe,
                           name=cots_name,
                           version=version,
                           cvss_min=cvss_min)

    response = Response("")
    response.headers['HX-Redirect'] = redirect_url
    return response


@resultPage.route('/results/cve')
def cve_results():
    user_cpe = request.args.get('cpe', '')
    cots_name = request.args.get('name', '')
    version = request.args.get('version', '')
    cvss_min = request.args.get('cvss_min', '0')
    print(f"On entre ici avec cost_name= { cots_name }")
    
    cves, exploits = [], {}
    searched = ""
    try: 
        if user_cpe and not cots_name:
            cves = fetch_cves_by_cpe(user_cpe, cvss_min)
            searched = user_cpe
        elif cots_name and not user_cpe:
            searched = cots_name
            if not version:
                cves = fetch_cves_by_name(cots_name, cvss_min)
            else:
                cves = fetch_cves_by_name_version(cots_name, version, cvss_min)
                searched += f' {version}'
        return render_template("base.html",
                            partial="partials/cve_results.html", 
                            cves=cves, 
                            exploits=exploits, 
                            searched=searched)
    except ConnectionError as e:
        return render_template("base.html",
                        partial="partials/error.html", 
                        message=str(e))
    


@resultPage.route('/results/cots')
def cots_results():
    guessed_name = request.args.get('guessed_name', '')
    guessed_provider = request.args.get('guessed_provider', '')

    
    if not guessed_name and not guessed_provider:
        print("OUCH")
        return redirect(url_for('searchPage.index'))
    try:
        # Logique de recherche
        if guessed_provider:
            cots_list = fetch_cots_by_guessed_provider(guessed_name, guessed_provider)
        else:
            cots_list = fetch_cots_by_guessed_name(guessed_name)
        return render_template("base.html", 
                            partial="partials/cots_results.html",
                            cots_list=cots_list, 
                            guessed_name=guessed_name)
    except ConnectionError as e:
        return render_template("base.html",
                        partial="partials/error.html", 
                        message=str(e))