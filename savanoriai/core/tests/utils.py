def errors(resp):
    if 'form' in resp.context:
        return resp.context['form'].errors
