import sys
import time
import urllib.error
import urllib.request
import asyncio

from functools import reduce as foldl


async def measure_download_speed(url: str) -> tuple[int, float]:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; SpeedTestScript/1.0)"}
    req = urllib.request.Request(url, headers=headers)

    try:
        start_time = time.perf_counter()

        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read()

        end_time = time.perf_counter()
    except urllib.error.URLError as e:
        print(f"Request failed: {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"Request encountered an error: {e}", file=sys.stderr)

    bytes_loaded = len(data)
    duration = end_time - start_time
    if duration == 0 or bytes_loaded == 0:
        raise ValueError

    return bytes_loaded, duration


async def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <URL>", file=sys.stderr)
        sys.exit(1)

    target_url = sys.argv[1]
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    try:
        results = await asyncio.gather(*[measure_download_speed(target_url) for _ in range(10)])
    except ValueError:
        print("At least one request failed to download data.", file=sys.stderr)
        sys.exit(1)

    total_bytes, total_duration = foldl(lambda acc, p: (acc[0] + p[0], acc[1] + p[1]), results)
    bytes_per_sec = total_bytes / total_duration
    mb_per_sec = bytes_per_sec / (1024 ** 2)
    mbps = (bytes_per_sec * 8) / 1_000_000

    print(
        f"Total Downloaded: {total_bytes:,} bytes\n"
        f"Total Time:       {total_duration:.4f} seconds\n"
        f"Average Speed:    {mbps:.2f} Mbps ({mb_per_sec:.2f} MB/s)"
    )


if __name__ == "__main__":
    asyncio.run(main())
