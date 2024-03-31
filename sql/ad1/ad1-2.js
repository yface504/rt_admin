// 引入 Supabase 客户端
const { createClient } = require('@supabase/supabase-js');

// 初始化 Supabase 客户端
const supabase = createClient('https://uwyrpfotwqobejfvsdlm.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3eXJwZm90d3FvYmVqZnZzZGxtIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNjI2MzY1NywiZXhwIjoyMDIxODM5NjU3fQ.z95ecttub0hf3ozLlEImGBaag80jZFX6HLtK6O1WERw');

// 定义 SQL 查询
const query = `
UPDATE ad1
SET
    cv = sd.cv,
    cv_include_free = sd.cv_include_free,
    ntd = sd.ntd
FROM (
    SELECT
        ad.agent,
        ad.source,
        sc.date::date,
        log.ad_full_code,
        COUNT(CASE WHEN sc.price > 0 THEN 1 END) AS cv,
        COUNT(*) AS cv_include_free,
        ROUND(SUM(sc.price) * 10) AS ntd
    FROM (
            SELECT ad_agency_code, date, price
            FROM sales_logs
            WHERE date BETWEEN '2024-03-01' AND '2024-03-24' and ad_agency_code IS NOT NULL
        ) sc
        JOIN cnt_logs log ON sc.ad_agency_code = log.ad_agency_code
        JOIN ad_codes ad ON log.ad_agency_code = ad.code
    WHERE
        ad.agent IS NOT NULL
        AND ad.source IS NOT NULL
        AND log.ad_full_code IS NOT NULL
    GROUP BY ad.agent, ad.source, sc.date, log.ad_full_code
) AS sd
WHERE
    ad1.agent = sd.agent AND
    ad1.source = sd.source AND
    ad1.date = sd.date AND
    ad1.ad = sd.ad_full_code;
`;

// 执行 SQL
async function runQuery() {
  let { data, error } = await supabase.rpc('your_function_name', { query: query });

  if (error) console.log('Error:', error);
  else console.log('Success:', data);
}

runQuery();
