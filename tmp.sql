with cats_dates as (
    select *
    from categories
    cross join dates
    where date_id in ({first_date_id}, {last_date_id})
)
select 
    cats_dates.category, 
    cats_dates.category_id, 
    cats_dates.date,
    count(prices.article)
from prices
join products
using (article)
join subcategories
on products.first_subcategory = subcategories.subcategory_id
right join cats_dates
    on subcategories.category_id = cats_dates.category_id
    and prices.date_id = cats_dates.date_id
group by cats_dates.category, cats_dates.category_id, cats_dates.date
order by cats_dates.category_id, cats_dates.date