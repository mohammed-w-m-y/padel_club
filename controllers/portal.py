from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class PadelCustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        """Add padel bookings count to the portal home page dashboard."""
        values = super()._prepare_home_portal_values(counters)
        if 'booking_count' in counters:
            partner = request.env.user.partner_id
            # Count bookings where the member's partner matches the current user
            booking_count = request.env['padel.booking'].sudo().search_count([
                ('member_id.partner_id', '=', partner.id)
            ]) if partner else 0
            values['booking_count'] = booking_count
        return values

    @http.route(['/my/bookings', '/my/bookings/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_bookings(self, page=1, sortby=None, filterby=None, **kw):
        """Render the list of bookings for the logged-in portal user."""
        vals = self._prepare_portal_layout_values()
        Booking = request.env['padel.booking'].sudo()
        partner = request.env.user.partner_id

        domain = [('member_id.partner_id', '=', partner.id)]

        # Sorting options
        searchbar_sortings = {
            'date': {'label': 'Newest', 'order': 'start_datetime desc'},
            'name': {'label': 'Court Name', 'order': 'court_id asc'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings.get(sortby, {}).get('order', 'start_datetime desc')

        # Pager configuration
        total_bookings = Booking.search_count(domain)
        pager = portal_pager(
            url="/my/bookings",
            total=total_bookings,
            page=page,
            step=10,
        )

        bookings = Booking.search(domain, order=order, limit=10, offset=pager['offset'])

        vals.update({
            'bookings': bookings,
            'page_name': 'booking',
            'pager': pager,
            'default_url': '/my/bookings',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render('padel_club.portal_my_bookings_list', vals)

    @http.route(['/my/bookings/<int:booking_id>'], type='http', auth='user', website=True)
    def portal_my_booking_detail(self, booking_id, **kw):
        """Render details for a specific booking with strict security access."""
        booking = request.env['padel.booking'].sudo().browse(booking_id)
        if not booking.exists():
            return request.not_found()

        # Security check: Ensure the booking belongs to the current logged-in user's partner
        partner = request.env.user.partner_id
        if booking.member_id.partner_id != partner:
            return request.render('website.403')

        vals = {
            'booking': booking,
            'page_name': 'booking',
        }
        return request.render('padel_club.portal_my_booking_detail', vals)