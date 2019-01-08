from functools import wraps, partial

# using convoluted name to really avoid namespace pollution
__rec_depth_kwargs_names = {
    'depth': '__rec_depth_current_depth',
    'default_return': '__rec_depth_default_return'
}


def rec_depth_limit(depth, default_return=0):
    """Decorator factory that limits the depth of the recursion for a function
        @:param depth - how many levels of recursive calls are allowed. Setting it to 0 means that none are allowed
            Note that this doesn't limit the number of calls, so if a function always does two recursive calls,
            then setting depth to n will produce 2^(n+1) calls to the function
        @:param default_return - the value return by any disallowed recursive call
    """

    def decorate(f, **kwargs):
        @wraps(f)
        def _decorator(*args, **kwargs):
            fkwargs = kwargs.copy()
            for i in __rec_depth_kwargs_names.values():
                fkwargs.pop(i)

            cur_depth = kwargs[__rec_depth_kwargs_names['depth']]
            if cur_depth[0] < 0:
                return kwargs[__rec_depth_kwargs_names['default_return']]
            else:
                cur_depth[0] -= 1
                rv = f(*args, **fkwargs)
                cur_depth[0] += 1
                return rv

        return partial(_decorator, **kwargs)

    cur_depth = [depth]  # using a list to make the int mutable
    values = [cur_depth, default_return]
    kwargs = dict(zip(__rec_depth_kwargs_names.values(), values))
    return partial(decorate, **kwargs)


__rec_call_limit_kwargs_names = {
    'number': '__rec_call_limit_number',
    'default_return': '__rec_call_limit_default_return'
}


def rec_call_limit(limit, default_return=0):
    """Decorator factory that limits the number of recursive calls for a function
        @:param limit - number of calls that will be allowed
        @:param default_return - the value return by any disallowed recursive call
    """

    def decorate(f, **kwargs):
        @wraps(f)
        def _decorator(*args, **kwargs):
            fkwargs = kwargs.copy()
            for i in __rec_call_limit_kwargs_names.values():
                fkwargs.pop(i)

            count = kwargs[__rec_call_limit_kwargs_names['number']]
            if count[0] < 0:
                return kwargs[__rec_call_limit_kwargs_names['default_return']]
            else:
                count[0] -= 1
                rv = f(*args, **fkwargs)
                return rv

        return partial(_decorator, **kwargs)

    count = [limit]
    values = [count, default_return]
    kwargs = dict(zip(__rec_call_limit_kwargs_names.values(), values))
    return partial(decorate, **kwargs)
