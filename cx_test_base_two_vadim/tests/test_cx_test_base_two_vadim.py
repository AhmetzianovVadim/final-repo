from odoo.tests.common import TransactionCase


class SomethingCase(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(SomethingCase, self).setUp(*args, **kwargs)

        # Create test partner
        self.test_partner = self.env["res.partner"].create({"name": "Test Partner"})

        # Create Products
        product = self.env["product.product"]

        self.product_1 = product.create({"name": "Product 1"})
        self.product_2 = product.create({"name": "Product 2"})
        self.product_3 = product.create({"name": "Product 3"})
        self.product_4 = product.create({"name": "Product 4"})

        # Create Sales Order
        self.sale_order_1 = self.env["sale.order"].create(
            {"name": "Sale Order #1", "partner_id": self.test_partner.id}
        )

        # Create Order Lines
        self.sale_order_line_1 = self.env["sale.order.line"].create(
            {
                "product_id": self.product_1.id,
                "order_id": self.sale_order_1.id,
                "name": self.product_1.name,
                "product_uom_qty": 1,
                "price_unit": 1,
            }
        )

        self.sale_order_line_2 = self.env["sale.order.line"].create(
            {
                "product_id": self.product_2.id,
                "order_id": self.sale_order_1.id,
                "name": self.product_2.name,
                "product_uom_qty": 1,
                "price_unit": 1,
            }
        )

        self.sale_order_line_3 = self.env["sale.order.line"].create(
            {
                "product_id": self.product_3.id,
                "order_id": self.sale_order_1.id,
                "name": self.product_3.name,
                "product_uom_qty": 1,
                "price_unit": 10,
            }
        )

    def test_default_sequences(self):
        # Check default sequence values

        self.assertEqual(
            self.sale_order_line_1.order_line_number,
            1,
            msg="Line number of the first line must be equal to 1",
        )

        self.assertEqual(
            self.sale_order_line_2.order_line_number,
            2,
            msg="Line number of the second line must be equal to 2",
        )

        self.assertEqual(
            self.sale_order_line_3.order_line_number,
            3,
            msg="Line number of the third line must be equal to 3",
        )

    def test_add_sequence(self):
        self.sale_order_line_4 = self.env["sale.order.line"].create(
            {
                "product_id": self.product_4.id,
                "order_id": self.sale_order_1.id,
                "name": self.product_4.name,
                "product_uom_qty": 1,
                "price_unit": 1,
            }
        )
        self.assertEqual(
            self.sale_order_line_4.order_line_number,
            4,
            msg="Line number of the fourth line must be equal to 4",
        )

    def test_delete_sequence(self):
        self.sale_order_line_2.unlink()
        self.assertEqual(
            self.sale_order_line_3.order_line_number,
            2,
            msg="Line number of the fourth line must be equal to 2",
        )

    def test_change_sequence(self):
        number = 10
        for rec in reversed(self.sale_order_1.order_line):
            rec.sequence = number
            number += 1
        self.assertEqual(
            self.sale_order_line_1.order_line_number,
            3,
            msg="Line number of the first line must be equal to 3",
        )
        self.assertEqual(
            self.sale_order_line_2.order_line_number,
            2,
            msg="Line number of the second line must be equal to 2",
        )
        self.assertEqual(
            self.sale_order_line_3.order_line_number,
            1,
            msg="Line number of the third line must be equal to 1",
        )
