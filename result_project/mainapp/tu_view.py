from django.shortcuts import render
from django.views.generic import View
from bs4 import BeautifulSoup
import requests
import urllib2


class TUFormView(View):
    template_name = 'tu_form.html'
    result_template = 'result.html'

    def get(self, request, *args, **kwargs):
        parameters = {}
        tu_faculties = self.get_tu_faculties()
        parameters['tu_faculties'] = tu_faculties
        return render(request, self.template_name, parameters)

    def get_tu_faculties(self):
        url = 'http://tu.ntc.net.np/result.php'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
        matches = soup.findAll('select', attrs={'name': 'faculty'})
        for match in matches:
            options = match.findAll('option')
            option_list = {i['value']: i.get_text() for i in options}
            return option_list

    def post(self, request, *args, **kwargs):
        parameters = {}
        url = 'http://tu.ntc.net.np/result.php'
        symbolno = request.POST.get('inputSymbolNo')
        parameters['symbolno'] = symbolno
        faculty = request.POST.get('faculty')
        parameters['faculty'] = faculty
        payload = {
            "faculty": faculty,
            "symbol": symbolno,
            "submit": 'Submit'
        }
        r = requests.post(url, payload)
        response_html = r.content
        soup = BeautifulSoup(response_html)
        matches = soup.findAll('div', attrs={'id': 'show-result'})
        for match in matches:
            parameters['result_content'] = str(match)
        parameters['another_result'] = 'tuform'
        return render(request, self.result_template, parameters)
