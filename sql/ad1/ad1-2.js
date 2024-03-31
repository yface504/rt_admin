  // updateAd1-2.js
const { Client } = require('pg');

async function updateAd1_2() {
  const client = new Client({
    connectionString: 'postgresql://postgres.uwyrpfotwqobejfvsdlm:z%23tLiUHu7zVkX.B@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres',
  });

  try {
    await client.connect();
    await client.query('SELECT public."ad1-2"();');
    console.log('Function executed successfully');
  } catch (err) {
    console.error('Error executing function:', err);
  } finally {
    await client.end();
  }
}

updateAd1_2();
