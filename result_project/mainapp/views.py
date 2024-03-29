from django.shortcuts import render
from django.views.generic import View
from bs4 import BeautifulSoup
import requests
import urllib2


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
        parameters['another_result'] = 'form'
        return render(request, self.result_template, parameters)

    def get_result(self, symbolno, dob=None):
        '''
        Function to get hseb result
        '''
        if dob is None:
            url = 'http://hseb.ntc.net.np/result.php'
            # url = 'http://slc.ntc.net.np/slc2070.php'
            payload = {
                "symbol": symbolno,
                "Submit": 'Submit'
            }
        else:
            url = 'http://hseb.ntc.net.np/markSheet.php'
# dob:2051/07/06
# no:20506169
# rem:PASS
# Submit:ShowMarks
            payload = {
                "no": symbolno,
                "dob": dob,
                # 'rem': 'PASS',
                "Submit": 'ShowMarks'
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
                remove = '(Date Format - YYYY/MM/DD example 2044/05/05 or 1983/04/25)'
                final_response = str(match).replace(remove, '')
                # return str(match)
                return final_response
            return '<p>Sorry ! Not found</p>'
        else:
            # for marksheet result
            matches = soup.findAll(
                'table'
                # attrs={
                #     'border': "1",
                #     'cellpadding': "15",
                #     'bgcolor': "#fcfcfc",
                #     'cellspacing': "0",
                #     'style': "border-collapse: collapse",
                #     'bordercolor': "#DDDDDD",
                #     'width': "100%"
                # }
            )
            for match in matches:
                return str(match)
            return '<p>Sorry ! The symbol number and date of birth do not match.</p>'
