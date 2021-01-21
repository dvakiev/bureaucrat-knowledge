import logging
from .test_common import TestBureaucratKnowledgeBase

_logger = logging.getLogger(__name__)


class TestBureaucratKnowledge(TestBureaucratKnowledgeBase):

    def test_category_default_values(self):
        self.demo_user.groups_id |= self.env.ref(
            'bureaucrat_knowledge.group_bureaucratic_knowledge_user')

        Category = self.env['bureaucrat.knowledge.category']
        category = Category.sudo(self.demo_user).create({
            'name': 'Test top level category',
        })

        self.assertEqual(category.visibility_type, 'restricted')
        self.assertEqual(len(category.owner_user_ids), 1)
        self.assertIn(self.demo_user, category.owner_user_ids)
        self.assertFalse(category.editor_user_ids)

        category.write({
            'editor_user_ids': [(6, 0, [self.demo_user.id])]})

        subcategory = Category.sudo(self.demo_user).create({
            'name': 'Test subcategory',
            'parent_id': category.id,
        })

        # Without this test does not pass. It seems that parent left/right are
        # not recomputed just after write
        self.env['bureaucrat.knowledge.category']._parent_store_compute()

        self.assertEqual(len(category.editor_user_ids), 1)
        self.assertEqual(len(category.actual_editor_user_ids), 1)
        self.assertIn(self.demo_user, category.editor_user_ids)
        self.assertIn(self.demo_user, category.actual_editor_user_ids)
        self.assertEqual(subcategory.visibility_type, 'parent')
        self.assertEqual(len(subcategory.owner_user_ids), 0)

        self.assertFalse(subcategory.editor_user_ids)
        self.assertEqual(len(subcategory.actual_editor_user_ids), 1)
        self.assertIn(self.demo_user, subcategory.actual_editor_user_ids)

        subcategory2 = Category.sudo(self.demo_user).create({
            'name': 'Test subcategory2',
            'parent_id': subcategory.id,
        })

        # Without this test does not pass. It seems that parent left/right are
        # not recomputed just after write
        self.env['bureaucrat.knowledge.category']._parent_store_compute()

        self.assertEqual(subcategory2.visibility_type, 'parent')
        self.assertEqual(len(subcategory2.owner_user_ids), 0)
        self.assertFalse(subcategory2.editor_user_ids)
        self.assertEqual(len(subcategory2.actual_editor_user_ids), 1)
        self.assertIn(self.demo_user, subcategory2.actual_editor_user_ids)

    def test_document_default_values(self):
        self.demo_user.groups_id |= self.env.ref(
            'bureaucrat_knowledge.group_bureaucratic_knowledge_user')

        Document = self.env['bureaucrat.knowledge.document']
        document = Document.sudo(self.demo_user).create({
            'name': 'Test top level document',
            'document_type': 'html',
        })

        self.assertEqual(document.visibility_type, 'restricted')
        self.assertEqual(len(document.owner_user_ids), 1)
        self.assertIn(self.demo_user, document.owner_user_ids)

        Category = self.env['bureaucrat.knowledge.category']
        category = Category.sudo(self.demo_user).create({
            'name': 'Test top level category2',
            'editor_user_ids': [(4, self.demo_user.id)],
        })

        subdocument = Document.sudo(self.demo_user).create({
            'name': 'Test top level document',
            'category_id': category.id,
            'document_type': 'html',
        })

        self.assertEqual(subdocument.visibility_type, 'parent')
        self.assertEqual(len(subdocument.owner_user_ids), 0)
        self.assertFalse(subdocument.editor_user_ids)
        self.assertEqual(len(subdocument.actual_editor_user_ids), 1)
        self.assertIn(self.demo_user, subdocument.actual_editor_user_ids)
