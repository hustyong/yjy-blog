export function onRequest(context) {
  const target = new URL("/redis", context.request.url);
  return Response.redirect(target.toString(), 302);
}
