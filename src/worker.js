// One host per site: www redirects to the apex (the canonical URL every page declares), which is
// what GitHub Pages did for us before the move. Everything else is a static file.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname.startsWith('www.')) {
      url.hostname = url.hostname.slice(4);
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
