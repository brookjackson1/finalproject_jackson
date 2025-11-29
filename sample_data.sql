-- Sample Data for NailsbyBrookJ
-- Run this after schema.sql to populate with realistic demo data

-- Sample Clients
INSERT INTO Clients (name, phone, instagram, email, allergies, notes) VALUES
('Sarah Johnson', '(555) 123-4567', '@sarahj_beauty', 'sarah.j@email.com', NULL, 'Loves pastel colors and minimalist designs'),
('Emily Rodriguez', '(555) 234-5678', '@emilyrnails', 'emily.r@email.com', 'Allergic to certain acrylic monomers', 'Prefers gel services, likes bold colors'),
('Jessica Chen', '(555) 345-6789', '@jesschen', 'jess.chen@email.com', NULL, 'Wedding client - loves French tips and elegant styles'),
('Amanda Martinez', '(555) 456-7890', NULL, 'amanda.m@email.com', NULL, 'Regular client, usually gets gel manicures every 3 weeks'),
('Lisa Thompson', '(555) 567-8901', '@lisathompson', 'lisa.t@email.com', NULL, 'Prefers short nails, natural look'),
('Rachel Kim', '(555) 678-9012', '@rachelk_nails', 'rachel.k@email.com', NULL, 'Loves nail art, especially geometric designs'),
('Megan Taylor', '(555) 789-0123', NULL, 'megan.t@email.com', 'Sensitive skin', 'Needs gentle products'),
('Olivia Brown', '(555) 890-1234', '@oliviab', 'olivia.b@email.com', NULL, 'Business professional - prefers nude and neutral tones'),
('Sophia Davis', '(555) 901-2345', '@sophiadnails', 'sophia.d@email.com', NULL, 'Loves seasonal designs and glitter'),
('Isabella Garcia', '(555) 012-3456', '@isabellag', 'isabella.g@email.com', NULL, 'Pedicure regular, likes bright summer colors');

-- Sample Appointments (mix of past and future)
INSERT INTO Appointments (client_id, service_id, appt_date, appt_time, price, status, notes, product_cost) VALUES
-- Past completed appointments
(1, 2, '2025-11-01', '10:00:00', 40.00, 'completed', 'Classic pink gel', 8.50),
(2, 4, '2025-11-03', '14:00:00', 65.00, 'completed', 'Natural gel extensions', 15.00),
(3, 1, '2025-11-05', '11:30:00', 25.00, 'completed', 'French manicure', 5.00),
(4, 2, '2025-11-08', '13:00:00', 40.00, 'completed', 'Red gel polish', 8.50),
(5, 7, '2025-11-10', '15:30:00', 35.00, 'completed', 'Basic pedicure', 10.00),
(6, 3, '2025-11-12', '10:30:00', 55.00, 'completed', 'Pink and white acrylics', 18.00),
(7, 2, '2025-11-15', '12:00:00', 40.00, 'completed', 'Nude gel', 8.50),
(1, 5, '2025-11-15', '14:30:00', 10.00, 'completed', 'Simple nail art - hearts', 2.00),
(8, 1, '2025-11-18', '09:00:00', 25.00, 'completed', 'Clear polish', 5.00),
(9, 2, '2025-11-20', '16:00:00', 40.00, 'completed', 'Sparkly holiday gel', 8.50),
(10, 7, '2025-11-22', '10:00:00', 35.00, 'completed', 'Summer pedicure', 10.00),
(2, 6, '2025-11-23', '13:30:00', 20.00, 'completed', 'Complex floral design', 3.00),
(3, 2, '2025-11-25', '11:00:00', 40.00, 'completed', 'Soft pink gel', 8.50),
(4, 3, '2025-11-27', '14:00:00', 55.00, 'completed', 'Natural acrylic set', 18.00),

-- Upcoming scheduled appointments
(1, 2, '2025-12-02', '10:00:00', 40.00, 'scheduled', 'Holiday design request', 0),
(5, 7, '2025-12-03', '15:00:00', 35.00, 'confirmed', 'Regular pedicure', 0),
(6, 3, '2025-12-05', '11:30:00', 55.00, 'scheduled', 'Fill appointment', 0),
(8, 1, '2025-12-06', '09:30:00', 25.00, 'confirmed', 'Simple manicure', 0),
(9, 6, '2025-12-08', '14:00:00', 20.00, 'scheduled', 'Winter snowflake design', 0),
(3, 2, '2025-12-10', '10:30:00', 40.00, 'scheduled', 'Wedding prep - trial', 0);

-- Initialize loyalty points for clients
INSERT INTO LoyaltyPoints (client_id, points, lifetime_points, last_earned) VALUES
(1, 9, 9, '2025-11-15'),
(2, 22, 22, '2025-11-23'),
(3, 13, 13, '2025-11-25'),
(4, 19, 19, '2025-11-27'),
(5, 7, 7, '2025-11-22'),
(6, 15, 15, '2025-11-12'),
(7, 4, 4, '2025-11-15'),
(8, 2, 2, '2025-11-18'),
(9, 8, 8, '2025-11-20'),
(10, 3, 3, '2025-11-22');

-- Sample Portfolio Photos
INSERT INTO PortfolioPhotos (image_url, title, description, appt_id) VALUES
('https://images.unsplash.com/photo-1604654894610-df63bc536371', 'Pink Ombre French', 'Soft pink to white ombre with classic French tips. Perfect for weddings!', 3),
('https://images.unsplash.com/photo-1610992015732-2449b76344bc', 'Red Velvet Glam', 'Deep red gel with matte finish and gold accent nail.', 4),
('https://images.unsplash.com/photo-1632345031435-8727f6897d53', 'Pastel Spring Vibes', 'Soft pastel colors with floral hand-painted details.', 1),
('https://images.unsplash.com/photo-1519014816548-bf5fe059798b', 'Classic French Manicure', 'Timeless elegance with perfect white tips.', NULL),
('https://images.unsplash.com/photo-1522338242992-e1a54906a8da', 'Geometric Black & Gold', 'Modern geometric patterns in black with gold leaf accents.', NULL),
('https://images.unsplash.com/photo-1606150534934-34845c339b80', 'Holiday Sparkle', 'Silver glitter ombre perfect for the holiday season.', 9),
('https://images.unsplash.com/photo-1609420713615-6ab815f183d0', 'Summer Coral Sunset', 'Vibrant coral and orange sunset gradient design.', 10),
('https://images.unsplash.com/photo-1607779097040-26e80aa78736', 'Nude Minimalist Chic', 'Subtle nude with single crystal accent nail.', 8);

-- Link portfolio photos to tags
INSERT INTO PhotoTags (photo_id, tag_id) VALUES
-- Photo 1: Pink Ombre French
(1, (SELECT tag_id FROM Tags WHERE name = 'French')),
(1, (SELECT tag_id FROM Tags WHERE name = 'Ombre')),
(1, (SELECT tag_id FROM Tags WHERE name = 'Pink')),
(1, (SELECT tag_id FROM Tags WHERE name = 'Wedding')),
(1, (SELECT tag_id FROM Tags WHERE name = 'Spring')),

-- Photo 2: Red Velvet Glam
(2, (SELECT tag_id FROM Tags WHERE name = 'Red')),
(2, (SELECT tag_id FROM Tags WHERE name = 'Matte')),
(2, (SELECT tag_id FROM Tags WHERE name = 'Glitter')),
(2, (SELECT tag_id FROM Tags WHERE name = 'Holiday')),

-- Photo 3: Pastel Spring
(3, (SELECT tag_id FROM Tags WHERE name = 'Pastel')),
(3, (SELECT tag_id FROM Tags WHERE name = 'Floral')),
(3, (SELECT tag_id FROM Tags WHERE name = 'Spring')),
(3, (SELECT tag_id FROM Tags WHERE name = 'Pink')),

-- Photo 4: Classic French
(4, (SELECT tag_id FROM Tags WHERE name = 'French')),
(4, (SELECT tag_id FROM Tags WHERE name = 'White')),
(4, (SELECT tag_id FROM Tags WHERE name = 'Glossy')),
(4, (SELECT tag_id FROM Tags WHERE name = 'Everyday')),

-- Photo 5: Geometric
(5, (SELECT tag_id FROM Tags WHERE name = 'Geometric')),
(5, (SELECT tag_id FROM Tags WHERE name = 'Black')),
(5, (SELECT tag_id FROM Tags WHERE name = 'Minimalist')),

-- Photo 6: Holiday Sparkle
(6, (SELECT tag_id FROM Tags WHERE name = 'Glitter')),
(6, (SELECT tag_id FROM Tags WHERE name = 'Chrome')),
(6, (SELECT tag_id FROM Tags WHERE name = 'Holiday')),
(6, (SELECT tag_id FROM Tags WHERE name = 'Winter')),

-- Photo 7: Summer Coral
(7, (SELECT tag_id FROM Tags WHERE name = 'Ombre')),
(7, (SELECT tag_id FROM Tags WHERE name = 'Summer')),
(7, (SELECT tag_id FROM Tags WHERE name = 'Red')),

-- Photo 8: Nude Minimalist
(8, (SELECT tag_id FROM Tags WHERE name = 'Nude')),
(8, (SELECT tag_id FROM Tags WHERE name = 'Minimalist')),
(8, (SELECT tag_id FROM Tags WHERE name = 'Everyday'));

-- Link services to inventory items
INSERT INTO ServiceItems (service_id, item_id, quantity_used) VALUES
-- Classic Manicure uses
((SELECT service_id FROM Services WHERE name = 'Classic Manicure'), (SELECT item_id FROM Inventory WHERE name = 'Base Coat'), 1),
((SELECT service_id FROM Services WHERE name = 'Classic Manicure'), (SELECT item_id FROM Inventory WHERE name = 'Top Coat'), 1),
((SELECT service_id FROM Services WHERE name = 'Classic Manicure'), (SELECT item_id FROM Inventory WHERE name = 'Cuticle Oil'), 0.5),
((SELECT service_id FROM Services WHERE name = 'Classic Manicure'), (SELECT item_id FROM Inventory WHERE name = 'Nail Files - 100 grit'), 1),

-- Gel Manicure uses
((SELECT service_id FROM Services WHERE name = 'Gel Manicure'), (SELECT item_id FROM Inventory WHERE name = 'Gel Base Coat'), 1),
((SELECT service_id FROM Services WHERE name = 'Gel Manicure'), (SELECT item_id FROM Inventory WHERE name = 'Gel Top Coat'), 1),
((SELECT service_id FROM Services WHERE name = 'Gel Manicure'), (SELECT item_id FROM Inventory WHERE name = 'Cuticle Oil'), 0.5),
((SELECT service_id FROM Services WHERE name = 'Gel Manicure'), (SELECT item_id FROM Inventory WHERE name = 'Nail Files - 100 grit'), 1),

-- Acrylic Full Set uses
((SELECT service_id FROM Services WHERE name = 'Acrylic Full Set'), (SELECT item_id FROM Inventory WHERE name = 'Acrylic Powder - Clear'), 20),
((SELECT service_id FROM Services WHERE name = 'Acrylic Full Set'), (SELECT item_id FROM Inventory WHERE name = 'Acrylic Liquid'), 2),
((SELECT service_id FROM Services WHERE name = 'Acrylic Full Set'), (SELECT item_id FROM Inventory WHERE name = 'Nail Files - 100 grit'), 2),
((SELECT service_id FROM Services WHERE name = 'Acrylic Full Set'), (SELECT item_id FROM Inventory WHERE name = 'Nail Buffer'), 1);
