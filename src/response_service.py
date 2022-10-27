class Paginate:

    @staticmethod
    def paginate(url, result, args, response):
        limit = 6 if args.get('limit') is None else int(args.get('limit'))
        offset = 0 if args.get('offset') is None else int(args.get('offset'))

        if len(result) < offset or limit < 0:
            response['data'] = []
            return

        response['offset'] = offset
        response['limit'] = limit

        if offset == 0:
            response['previous'] = ""
        else:
            start_cpy = max(0, offset - limit)
            response['previous'] = url + '?offset=%d&limit=%d' % (start_cpy, limit)

        if offset + limit > len(result):
            response['next'] = ""
        else:
            start_cpy = offset + limit
            response['next'] = url + '?offset=%d&limit=%d' % (start_cpy, limit)

        response['data'] = result[offset:offset + limit]

        return response

    @staticmethod
    def link_request_to_participants_by_id(response):
        for entry in response["data"]:
            if "links" not in entry:
                entry["links"] = {}
            req_id = entry["request_id"]
            entry["links"]["participants"] = "/requests/{id}/participants".format(id=req_id)
        return response

    @staticmethod
    def link_participant_to_user_by_id(response):
        for entry in response["data"]:
            if "links" not in entry:
                entry["links"] = {}
            user_id = entry["user_id"]
            entry["links"]["user"] = "/users/{id}".format(id=user_id)
        return response
