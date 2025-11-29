-- Historical Appointment Data for Revenue Trend
-- Adds completed appointments from July - October 2025

-- July 2025 (8 appointments, ~$340 revenue)
INSERT INTO Appointments (client_id, service_id, appt_date, appt_time, price, status, notes, product_cost) VALUES
(1, 2, '2025-07-05', '10:00:00', 40.00, 'completed', 'Summer coral gel', 8.50),
(2, 1, '2025-07-08', '14:00:00', 25.00, 'completed', 'Classic manicure', 5.00),
(3, 7, '2025-07-12', '11:00:00', 35.00, 'completed', 'Beach pedicure', 10.00),
(4, 2, '2025-07-15', '13:30:00', 40.00, 'completed', 'Bright pink gel', 8.50),
(5, 3, '2025-07-18', '10:30:00', 55.00, 'completed', 'New acrylic set', 18.00),
(6, 2, '2025-07-22', '15:00:00', 40.00, 'completed', 'Red gel polish', 8.50),
(7, 1, '2025-07-25', '12:00:00', 25.00, 'completed', 'Quick manicure', 5.00),
(8, 4, '2025-07-28', '14:30:00', 65.00, 'completed', 'Gel extensions', 15.00);

-- August 2025 (12 appointments, ~$520 revenue - business growing)
INSERT INTO Appointments (client_id, service_id, appt_date, appt_time, price, status, notes, product_cost) VALUES
(1, 2, '2025-08-02', '10:00:00', 40.00, 'completed', 'Vacation nails', 8.50),
(2, 3, '2025-08-05', '14:00:00', 55.00, 'completed', 'Back to school acrylics', 18.00),
(3, 2, '2025-08-08', '11:30:00', 40.00, 'completed', 'Peach gel', 8.50),
(4, 1, '2025-08-10', '13:00:00', 25.00, 'completed', 'Classic manicure', 5.00),
(5, 7, '2025-08-12', '15:00:00', 35.00, 'completed', 'Summer pedicure', 10.00),
(6, 6, '2025-08-14', '10:30:00', 20.00, 'completed', 'Floral nail art', 3.00),
(7, 2, '2025-08-17', '12:30:00', 40.00, 'completed', 'Purple gel', 8.50),
(8, 4, '2025-08-20', '14:00:00', 65.00, 'completed', 'Gel extensions with art', 15.00),
(9, 2, '2025-08-23', '11:00:00', 40.00, 'completed', 'Nude gel', 8.50),
(10, 1, '2025-08-26', '13:30:00', 25.00, 'completed', 'Quick refresh', 5.00),
(1, 7, '2025-08-28', '10:00:00', 35.00, 'completed', 'Spa pedicure', 10.00),
(3, 5, '2025-08-30', '15:00:00', 10.00, 'completed', 'Accent nail art', 2.00);

-- September 2025 (15 appointments, ~$630 revenue - peak season)
INSERT INTO Appointments (client_id, service_id, appt_date, appt_time, price, status, notes, product_cost) VALUES
(1, 2, '2025-09-03', '10:00:00', 40.00, 'completed', 'Fall colors gel', 8.50),
(2, 4, '2025-09-05', '14:00:00', 65.00, 'completed', 'Gel extensions', 15.00),
(3, 3, '2025-09-07', '11:00:00', 55.00, 'completed', 'Acrylic fill', 18.00),
(4, 2, '2025-09-10', '13:30:00', 40.00, 'completed', 'Burgundy gel', 8.50),
(5, 1, '2025-09-12', '15:00:00', 25.00, 'completed', 'Classic manicure', 5.00),
(6, 2, '2025-09-14', '10:30:00', 40.00, 'completed', 'Fall orange gel', 8.50),
(7, 7, '2025-09-17', '12:00:00', 35.00, 'completed', 'Luxury pedicure', 10.00),
(8, 6, '2025-09-19', '14:30:00', 20.00, 'completed', 'Autumn leaves design', 3.00),
(9, 2, '2025-09-21', '11:00:00', 40.00, 'completed', 'Plum gel', 8.50),
(10, 3, '2025-09-23', '13:00:00', 55.00, 'completed', 'New acrylic set', 18.00),
(1, 5, '2025-09-25', '15:30:00', 10.00, 'completed', 'Fall nail art', 2.00),
(2, 2, '2025-09-27', '10:00:00', 40.00, 'completed', 'Dark red gel', 8.50),
(4, 7, '2025-09-28', '14:00:00', 35.00, 'completed', 'Relaxing pedicure', 10.00),
(5, 4, '2025-09-29', '11:30:00', 65.00, 'completed', 'Gel extensions', 15.00),
(6, 5, '2025-09-30', '16:00:00', 10.00, 'completed', 'Simple accent art', 2.00);

-- October 2025 (16 appointments, ~$710 revenue - continued growth)
INSERT INTO Appointments (client_id, service_id, appt_date, appt_time, price, status, notes, product_cost) VALUES
(1, 2, '2025-10-02', '10:00:00', 40.00, 'completed', 'Halloween prep', 8.50),
(2, 3, '2025-10-04', '14:00:00', 55.00, 'completed', 'Acrylic fill', 18.00),
(3, 2, '2025-10-06', '11:30:00', 40.00, 'completed', 'Orange and black gel', 8.50),
(4, 1, '2025-10-08', '13:00:00', 25.00, 'completed', 'Quick manicure', 5.00),
(5, 7, '2025-10-10', '15:00:00', 35.00, 'completed', 'Fall pedicure', 10.00),
(6, 6, '2025-10-12', '10:30:00', 20.00, 'completed', 'Halloween nail art', 3.00),
(7, 2, '2025-10-14', '12:00:00', 40.00, 'completed', 'Deep purple gel', 8.50),
(8, 4, '2025-10-16', '14:30:00', 65.00, 'completed', 'Gel extensions', 15.00),
(9, 2, '2025-10-18', '11:00:00', 40.00, 'completed', 'Spooky design gel', 8.50),
(10, 3, '2025-10-20', '13:30:00', 55.00, 'completed', 'New acrylic set', 18.00),
(1, 6, '2025-10-22', '15:00:00', 20.00, 'completed', 'Pumpkin nail art', 3.00),
(2, 2, '2025-10-24', '10:00:00', 40.00, 'completed', 'Dark burgundy gel', 8.50),
(3, 7, '2025-10-26', '14:00:00', 35.00, 'completed', 'Pre-holiday pedicure', 10.00),
(4, 2, '2025-10-28', '11:30:00', 40.00, 'completed', 'Halloween party nails', 8.50),
(5, 4, '2025-10-30', '13:00:00', 65.00, 'completed', 'Gel extensions with art', 15.00),
(6, 5, '2025-10-31', '16:00:00', 10.00, 'completed', 'Halloween design', 2.00);
