const rolePermissions = {
  Visitor: ['view_cases', 'submit_clues', 'view_home'],
  Related: ['view_cases', 'submit_clues', 'view_progress', 'view_home'],
  Officer: ['view_cases', 'submit_clues', 'view_progress', 'update_progress', 'view_residents', 'view_home'],
  Cid: ['view_cases', 'submit_clues', 'view_progress', 'update_progress', 'view_residents', 'manage_cases', 'view_home'],
  Admin: ['view_cases', 'submit_clues', 'view_progress', 'update_progress', 'view_residents', 'manage_cases', 'manage_users', 'view_home']
};

export const hasPermission = (role, permission) => {
  if (permission === 'view_home') return true;
  if (!role || !rolePermissions[role]) return false;
  return rolePermissions[role].includes(permission);
}; 