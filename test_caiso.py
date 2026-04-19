import asyncio, httpx, pandas as pd, zipfile, io, csv
async def run():
    start = pd.Timestamp.utcnow()-pd.Timedelta(days=30)
    end = pd.Timestamp.utcnow()
    params={'queryname':'PRC_LMP','market_run_id':'DAM','startdatetime':start.strftime('%Y%m%dT07:00-0000'),'enddatetime':end.strftime('%Y%m%dT07:00-0000'),'node':'PALOVRDE_ASR-APND','resultformat':6,'version':1}
    async with httpx.AsyncClient() as c:
        r=await c.get('http://oasis.caiso.com/oasisapi/SingleZip',params=params, follow_redirects=True)
        print("Status", r.status_code)
        try:
            z = zipfile.ZipFile(io.BytesIO(r.content))
            for name in z.namelist():
                print(name)
                with z.open(name) as f:
                    c = f.read().decode('utf-8')
                    print(len(c.split('\n')), "lines in CSV")
        except Exception as e:
            print("Zip error", e, r.content[:200])
asyncio.run(run())
