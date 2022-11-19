import asyncio
import json

import asyncclick
import httpx
import validators

client = httpx.AsyncClient()

METHODS = ('GET', 'POST', 'PUT', 'PATCH',
           'DELETE', 'HEAD', 'OPTIONS')


async def make_request(url: str, method: str):
    headers = {
        "Accept": "application/json"
    }
    request = client.build_request(
        method=method,
        url=url,
        headers=headers
    )
    response = await client.send(request, stream=True)
    status_code = response.status_code
    return status_code


async def survey_url(url: str):
    methods_dict = dict()
    for method in METHODS:
        status_code = await make_request(url, method)
        if status_code == 404:
            return 404
        if status_code != 405:
            methods_dict[method] = status_code
    return methods_dict


@asyncclick.command()
@asyncclick.argument('strings', nargs=-1)
async def main(strings):
    output = dict()
    for string in strings:
        if validators.url(string):
            result = await survey_url(string)
            if result == 404:
                output[string] = 'Not found'
            else:
                output[string] = result
        else:
            output[string] = 'Not correct url item'
    result = json.dumps(output, indent=4)
    print(result)
    return result


if __name__ == '__main__':
    asyncio.run(main())
