from django.shortcuts import render
from django.views.generic import View
# from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
# import urllib
import urllib2
# import cookielib


class FormView(View):
    template_name = 'form.html'
    result_template = 'result.html'

    def get(self, request, *args, **kwargs):
        parameters = {}
        parameters['coming_soon'] = False
        url = 'http://hseb.ntc.net.np/'
        req = urllib2.Request(url)
        rsp = urllib2.urlopen(req)
        content = rsp.read()

        # testing for tu result
        # tu_faculties = self.get_tu_faculties()
        # self.get_tu_result(tu_faculties)
        if 'coming soon' in content:
            parameters['coming_soon'] = True
        # parameters['coming_soon'] = False   # for testing only
        return render(request, self.template_name, parameters)

    def post(self, request, *args, **kwargs):
        parameters = {}
        symbolno = request.POST.get('inputSymbolNo')
        parameters['symbolno'] = symbolno
        dob = request.POST.get('inputDOB')
        parameters['dob'] = dob
        if dob == '':
            content = self.get_result(symbolno)
        else:
            content = self.get_result(symbolno, dob)
        parameters['result_content'] = content
        return render(request, self.result_template, parameters)

    def get_result(self, symbolno, dob=None):
        '''
        Function to get hseb result
        '''
        if dob is None:
            # url = 'http://hseb.ntc.net.np/'
            url = 'http://slc.ntc.net.np/slc2070.php'
            payload = {
                "symbol": symbolno,
                "Submit": 'Submit'
            }
        else:
            url = 'http://slc.ntc.net.np/slc2070_ledger.php'
            payload = {
                "symbol": symbolno,
                "dob": dob,
                "submit": 'Submit'
            }
        # headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            r = requests.post(url, payload)
        except:
            return '<p>Sorry ! The symbol number and date of birth do not match</p>'

        # start parsing the response with beautifulsoap4
        response_html = r.content
        soup = BeautifulSoup(response_html)

        if dob is None:
            # for pass-fail result
            matches = soup.findAll('div', attrs={'id': 'show-result'})
            for match in matches:
                return str(match)
            return '<p>Sorry ! Not found</p>'
        else:
            # for marksheet result
            matches = soup.findAll(
                'table',
                attrs={
                    'border': "1",
                    'cellpadding': "15",
                    'bgcolor': "#fcfcfc",
                    'cellspacing': "0",
                    'style': "border-collapse: collapse",
                    'bordercolor': "#DDDDDD",
                    'width': "100%"
                }
            )
            for match in matches:
                return str(match)
            return '<p>Sorry ! The symbol number and date of birth do not match.</p>'

    def get_tu_faculties(self):
        url = 'http://tu.ntc.net.np/result.php'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
        matches = soup.findAll('select', attrs={'name': 'faculty'})
        for match in matches:
            # print ('Element: {0} , {1}'.format(type(matches), matches[0]))
            options = match.findAll('option')
            option_list = {i['value']: i.get_text() for i in options}
            return option_list

    def get_tu_result(self, tu_faculties):
        url = 'http://tu.ntc.net.np/result.php'
        # print tu_faculties
        payload = {
            "faculty": 112,
            "symbol": 2113824,
            "submit": 'Submit'
        }
        r = requests.post(url, payload)
        response_html = r.content
        soup = BeautifulSoup(response_html)
        matches = soup.findAll('div', attrs={'id': 'show-result'})
        for match in matches:
            print str(match)
        # return '<p>Sorry ! Not found</p>'
