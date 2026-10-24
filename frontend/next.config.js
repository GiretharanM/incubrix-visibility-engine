/** @type {import('next').NextConfig} */
const isStaticExport = process.env.STATIC_EXPORT === 'true';

const nextConfig = {
  reactStrictMode: true,
  ...(isStaticExport ? {
    output: 'export',
    basePath: process.env.NEXT_PUBLIC_BASE_PATH || '',
    images: { unoptimized: true },
    trailingSlash: true,
  } : {
    async rewrites() {
      return [
        {
          source: '/api/:path*',
          destination: 'http://localhost:8001/api/:path*',
        },
      ]
    },
  }),
}

module.exports = nextConfig
