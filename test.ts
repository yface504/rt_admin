const formattedDate = new Date(new Date().setDate(new Date().getDate() - 1)).toISOString().split('T')[0] + ' 23:59:59';
console.log(formattedDate)