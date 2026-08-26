-- Example data for local development.
-- Safe to run more than once.

INSERT INTO news_category (name, sort_order) VALUES
('Top Stories', 1),
('World', 2),
('Technology', 3),
('Business', 4),
('Sports', 5),
('Entertainment', 6),
('Science', 7),
('Health', 8)
ON CONFLICT (name) DO UPDATE
SET sort_order = EXCLUDED.sort_order;

INSERT INTO news (title, description, content, image, author, category_id, views, publish_time)
SELECT
    item.title,
    item.description,
    item.content,
    item.image,
    item.author,
    category.id,
    item.views,
    item.publish_time::timestamp
FROM (
    VALUES
    (
        'Global Climate Summit Opens With New Funding Pledge',
        'World leaders announce a new fund for climate adaptation projects.',
        'Delegates from more than 100 countries opened the summit with a focus on resilience, infrastructure, and long-term emissions reductions. The new fund is expected to support flood prevention, clean energy upgrades, and agricultural adaptation programs.',
        'https://picsum.photos/id/1015/600/400',
        'News Set Desk',
        'Top Stories',
        1280,
        '2026-01-10 09:00:00'
    ),
    (
        'New Satellite Network Expands Rural Internet Coverage',
        'A communications provider begins service in remote regions.',
        'The network is designed to improve broadband access for schools, clinics, and small businesses in areas where fiber deployment remains difficult. Early trials reported stable speeds during peak usage hours.',
        'https://picsum.photos/id/180/600/400',
        'Technology Reporter',
        'Technology',
        940,
        '2026-01-11 12:30:00'
    ),
    (
        'Markets Close Higher After Strong Earnings Reports',
        'Technology and industrial shares led the major indexes upward.',
        'Investors responded to stronger-than-expected quarterly earnings and improved guidance from several large companies. Analysts said the results eased concerns about slowing demand in key sectors.',
        'https://picsum.photos/id/1060/600/400',
        'Business Desk',
        'Business',
        760,
        '2026-01-12 16:45:00'
    ),
    (
        'City Marathon Draws Record Number of Runners',
        'More than 40,000 participants joined the annual race.',
        'Organizers said this year saw the largest field in the event history, with runners from dozens of countries. The route passed major landmarks and finished downtown in front of a large crowd.',
        'https://picsum.photos/id/249/600/400',
        'Sports Desk',
        'Sports',
        520,
        '2026-01-13 08:15:00'
    ),
    (
        'Researchers Announce Progress on Battery Recycling',
        'A new process could recover more material from used batteries.',
        'The research team said the method reduces chemical waste and improves recovery rates for lithium, nickel, and cobalt. Commercial testing is planned with several manufacturing partners.',
        'https://picsum.photos/id/201/600/400',
        'Science Desk',
        'Science',
        610,
        '2026-01-14 10:20:00'
    )
) AS item(title, description, content, image, author, category_name, views, publish_time)
JOIN news_category AS category ON category.name = item.category_name
WHERE NOT EXISTS (
    SELECT 1
    FROM news
    WHERE news.title = item.title
);
